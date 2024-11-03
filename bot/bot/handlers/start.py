from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager

router = Router()


@router.message(CommandStart())
async def cmd_start(_: types.Message, dialog_manager: DialogManager):
    pass
