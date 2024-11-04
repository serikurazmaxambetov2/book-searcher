from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Case, Const

from ..services import api_service


async def on_next_click(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик клика на кнопку следующей страницы"""
    data = dialog_manager.dialog_data

    current_page: int = data.get("current_page")  # type: ignore
    max_page: int = data.get("max_page")  # type: ignore
    text = data.get("text")

    if current_page < max_page:
        # Обновляем счетчик страницы и получаем данные с backend
        current_page += 1
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


next_page_button = Button(
    Case(
        {True: Const(">"), False: Const("-")},
        # Если текущая страница != последней то текст >, иначе -
        selector=F["dialog_data"]["current_page"] != F["dialog_data"]["max_page"],
    ),
    on_click=on_next_click,
    id="next_page_btn",
)
