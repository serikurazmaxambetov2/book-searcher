from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager

from ..states.main import MainSG

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: types.Message, dialog_manager: DialogManager):
    await msg.delete()
    await dialog_manager.start(state=MainSG.MAIN)
