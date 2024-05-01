from aiogram.fsm.state import State, StatesGroup


class MakingOrder(StatesGroup):
    title = State()
    mark = State()
    rate = State()
    comment = State()
    email = State()
    confirm = State()
