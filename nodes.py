from aiogram.types import Message
from keyboards import node_keyboard
from state import get_user_state

NODES = {
    "start": {
        "text": (
            "🌙 Вечер был тёплым.\n\n"
            "Ты шла по аллее парка.\n"
            "Фонари загорались один за другим."
        ),
        "actions": {
            "🚶‍♀️ Идти дальше": "alley_noise"
        }
    },

    "alley_noise": {
        "text": (
            "Ты сделала несколько шагов.\n\n"
            "Вдруг — треск веток в кустах справа."
        ),
        "actions": {
            "👀 Посмотреть в кусты": "bushes",
            "🚶‍♀️ Пройти мимо": "walk_past"
        }
    },

    "bushes": {
        "text": "Ты раздвигаешь кусты и видишь что-то странное…",
        "actions": {
            "➡️ Пойти дальше": "walk_past"
        }
    },

    "walk_past": {
        "text": "Ты идёшь дальше по аллее, чувствуя лёгкое волнение.",
        "actions": {}
    }
}

async def send_node(message: Message, node_id: str):
    user = get_user_state(message.from_user.id)
    user["node"] = node_id
    node = NODES[node_id]

    await message.answer(
        node["text"],
        reply_markup=node_keyboard(node["actions"])
    )
