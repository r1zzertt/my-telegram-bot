from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def node_keyboard(actions: dict):
    keyboard = []
    for text, node_id in actions.items():
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"node:{node_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
