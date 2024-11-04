import math

from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Row
from aiogram_dialog.widgets.text import Case, Const, Format, List, Multi

from ..keyboards import next_page_button, prev_page_button
from ..services import api_service
from ..states.main import MainSG


async def on_success(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, data: str
):
    await message.delete()

    # Получаем данные с backend
    response = await api_service.search(data)
    total = response.get("total")
    items = [(index, item) for index, item in enumerate(response.get("data"), start=1)]

    # Обновляем состояние
    dialog_manager.dialog_data["text"] = data
    dialog_manager.dialog_data["total"] = total
    dialog_manager.dialog_data["items"] = items
    dialog_manager.dialog_data["current_page"] = 1
    dialog_manager.dialog_data["max_page"] = math.ceil(total / 10)
    dialog_manager.dialog_data["is_not_empty"] = total != 0

    # Переходим к следующему состоянию
    await dialog_manager.next(ShowMode.EDIT)


async def getter(dialog_manager: DialogManager, **_):
    return dialog_manager.dialog_data


main_dialog = Dialog(
    Window(
        Const("Введите слово для поиска:"),
        TextInput(on_success=on_success, id="search_input"),
        state=MainSG.MAIN,
    ),
    Window(
        Case(
            {
                False: Const("Совпадений нет"),
                True: Multi(
                    Const("Вот совпадения:"),
                    List(
                        Format("{item[0]}. {item[1][title]}"),
                        items="items",
                    ),
                    sep="\n\n",
                ),
            },
            selector="is_not_empty",
        ),
        Row(
            prev_page_button,
            Button(Format("{current_page} | {max_page}"), id="current_page"),
            next_page_button,
            when="is_not_empty",
        ),
        Back(Const("Назад")),
        getter=getter,
        state=MainSG.SEARCH,
    ),
)
