from aiogram import Router

from .main import main_dialog

dialog_register = Router()
dialog_register.include_router(main_dialog)
