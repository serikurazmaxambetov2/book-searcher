from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Case, Const

from ..services import api_service


async def on_click(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data

    current_page: int = data.get("current_page")  # type: ignore
    text = data.get("text")

    if current_page - 1 > 0:
        current_page -= 1
        response = await api_service.search(
            text,  # type: ignore
            current_page,
        )

        # Конвертируем items в (item_id, item)
        items = [
            ((current_page - 1) * 10 + index, item)
            for index, item in enumerate(response.get("data"), start=1)
        ]

        # Обновляем состояние
        data["items"] = items
        data["current_page"] = current_page
        await dialog_manager.update(data)


prev_page_button = Button(
    Case(
        {False: Const("<"), True: Const("-")},
        # Если текущая страница == 1 то текст кнопки -, иначе <
        selector=F["dialog_data"]["current_page"] == 1,
    ),
    on_click=on_click,
    id="prev_page_btn",
)
