from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from ..states.main import MainSG


async def on_success(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, data: str
):
    # Обработка...
    pass
    # ...


main_dialog = Dialog(
    Window(
        Const("Введите слово для поиска:"),
        TextInput(on_success=on_success, id="search_input"),
        state=MainSG.MAIN,
    )
)
