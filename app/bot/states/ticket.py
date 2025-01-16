from aiogram.fsm.state import State, StatesGroup


class CreateTicketStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_title = State()
    waiting_for_description = State()