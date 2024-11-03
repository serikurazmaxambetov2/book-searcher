from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const

from ..services import api_service
from ..states.main import MainSG


async def on_success(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, data: str
):
    # Обработка...
    response = await api_service.search(data)
    total = response.get("total")
    items = response.get("data")

    await dialog_manager.update(
        {"total": total, "items": items, "current_page": 1, "max_page": total // 10 + 1}
    )
    await dialog_manager.switch_to(MainSG.SEARCH)
    # ...


main_dialog = Dialog(
    Window(
        Const("Введите слово для поиска:"),
        TextInput(on_success=on_success, id="search_input"),
        state=MainSG.MAIN,
    )
)
