from aiogram import Router

from .start import router as start_cmd_router

router = Router()
router.include_router(start_cmd_router)
