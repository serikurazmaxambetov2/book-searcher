from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    MAIN = State()
    SEARCH = State()
