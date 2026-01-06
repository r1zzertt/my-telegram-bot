import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import BOT_TOKEN, ADMIN_ID
from nodes.story import send_node
from state import reset_user, get_user_state, clear_wait
from inventory import inventory_text
from voices import save_voice

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# =====================
# /start
# =====================
@router.message(Command("start"))
async def start_handler(message: Message):
    reset_user(message.from_user.id)
    await message.answer("Я жив 🚀")
    await send_node(message, "start")

# =====================
# КНОПКИ
# =====================
@router.callback_query()
async def callbacks(callback: CallbackQuery):
    user = get_user_state(callback.from_user.id)

    if callback.data == "inventory":
        await callback.answer()
        await callback.message.answer(
            inventory_text(user)
        )
        return

    if callback.data.startswith("node:"):
        node_id = callback.data.split(":", 1)[1]
        await callback.message.delete()
        await send_node(callback.message, node_id)

# =====================
# СОХРАНЕНИЕ ГОЛОСА (АДМИН)
# =====================
@router.message()
async def admin_commands(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text and message.text.startswith("/save"):
        key = message.text.split(" ", 1)[1]
        admin = get_user_state(ADMIN_ID)
        admin["wait_voice"] = key
        await message.answer(f"🎙 Жду голос для ключа: {key}")

# =====================
# ГОЛОС
# =====================
@router.message()
async def voice_handler(message: Message):
    if not message.voice:
        return

    user = get_user_state(message.from_user.id)

    # админ сохраняет голос
    if message.from_user.id == ADMIN_ID:
        if user.get("wait_voice"):
            save_voice(user["wait_voice"], message.voice.file_id)
            clear_wait(user)
            await message.answer("💾 Голос сохранён")
            return

# =====================
# ЗАПУСК
# =====================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
