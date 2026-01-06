import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import BOT_TOKEN, ADMIN_ID
from nodes.story import NODES, CAT_ACTIONS, TREE_ACTIONS
from state import reset_user, get_user_state, wait_for_voice
from inventory import inventory_text, add_item, remove_item
from voices import save_voice
from keyboards import node_keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# =====================
# /start
# =====================

@router.message(Command("start"))
async def start_handler(message: Message):
    try:
        reset_user(message.from_user.id)
        await message.answer("Парк, который помнит🌹")
        await send_node(message, "start")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


# =====================
# CALLBACKS
# =====================
@router.callback_query()
async def callbacks(callback: CallbackQuery):
    user = get_user_state(callback.from_user.id)
    data = callback.data

    if data == "inventory":
        await callback.answer()
        await callback.message.answer(inventory_text(user))
        return

    if data.startswith("node:"):
        node_id = data.split(":", 1)[1]
        await callback.answer()
        await send_node(callback.message, node_id)

# =====================
# АДМИН-КОМАНДЫ
# =====================
@router.message(lambda m: m.from_user.id == ADMIN_ID and m.text and m.text.startswith("/save"))
async def admin_commands(message: Message):
    key = message.text.split(" ", 1)[1]
    admin = get_user_state(ADMIN_ID)
    admin["wait_voice"] = key
    await message.answer(f"🎙 Жду голос для ключа: {key}")

# =====================
# ОБРАБОТКА ГОЛОСА
# =====================
@router.message(lambda m: m.voice is not None)
async def voice_handler(message: Message):
    user = get_user_state(message.from_user.id)
    if message.from_user.id == ADMIN_ID and user.get("wait_voice"):
        save_voice(user["wait_voice"], message.voice)
        user["wait_voice"] = None
        await message.answer("🎙 Голос сохранён")
    else:
        await message.answer("🌫 Голос принят")

# =====================
# SEND NODE
# =====================
async def send_node(message: Message, node_id: str):
    user = get_user_state(message.from_user.id)

    if node_id == "act11_branch":
        if "🐶 Щенок" in user.get("inventory", []):
            await send_node(message, "act11_with_puppy")
        else:
            await send_node(message, "act11_without_puppy")
        return

    if node_id in CAT_ACTIONS:
        await message.answer(CAT_ACTIONS[node_id])
        hub = NODES["cat_hub"]
        await message.answer(hub["text"], reply_markup=node_keyboard(hub["actions"]))
        return

    if node_id in TREE_ACTIONS:
        await message.answer(TREE_ACTIONS[node_id])
        return

    node = NODES.get(node_id)
    if not node:
        await message.answer("Что-то пошло не так… 🌫")
        return

    user["node"] = node_id

    if node_id == "cat_hub":
        add_item(user, "🌸 Цветок тишины")
    if node_id == "puppy_take":
        add_item(user, "🐶 Щенок")

    await message.answer(
        node["text"],
        reply_markup=node_keyboard(node.get("actions", {}))
    )

# =====================
# RUN BOT
# =====================
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
