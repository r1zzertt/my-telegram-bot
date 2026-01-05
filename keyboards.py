from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def node_keyboard(actions: dict, show_inventory=True):
    keyboard = []

    for text, data in actions.items():
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=data
            )
        ])

    if show_inventory:
        keyboard.append([
            InlineKeyboardButton(
                text="🎒 Инвентарь",
                callback_data="inventory"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
