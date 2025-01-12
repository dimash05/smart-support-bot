from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/faq"),
                KeyboardButton(text="/new_ticket"),
            ],
            [
                KeyboardButton(text="/my_tickets"),
                KeyboardButton(text="/help"),
            ],
        ],
        resize_keyboard=True,
    )