import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, ADMIN_ID
from nodes import send_node
from state import reset_user, get_user_state, clear_wait, users
from inventory import inventory_text
from voices import save_voice

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =====================
# /start
# =====================
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    reset_user(message.from_user.id)
    await send_node(message, "start")


# =====================
# КНОПКИ
# =====================
@dp.callback_query()
async def callbacks(callback: CallbackQuery):
    user = get_user_state(callback.from_user.id)

    if callback.data == "inventory":
        await callback.answer()
        await callback.message.answer(inventory_text(user))
        return

    if callback.data.startswith("node:"):
        node_id = callback.data.split(":")[1]
        await callback.message.delete()
        await send_node(callback.message, node_id)


# =====================
# СОХРАНЕНИЕ ГОЛОСА (АДМИН)
# =====================
@dp.message(F.text.startswith("/save"))
async def save_voice_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    key = message.text.split(" ", 1)[1]
    admin = get_user_state(ADMIN_ID)
    admin["wait_voice"] = key
    await message.answer(f"🎙 Жду голос для ключа: {key}")


# =====================
# ГОЛОСОВЫЕ
# =====================
@dp.message(F.voice)
async def voice_handler(message: Message):
    user = get_user_state(message.from_user.id)

    # админ — сохраняет голос
    if message.from_user.id == ADMIN_ID:
        if user.get("wait_voice"):
            save_voice(user["wait_voice"], message.voice.file_id)
            clear_wait(user)
            await message.answer("💾 Голос сохранён")
            return

    # отправка живого голоса игроку
    for uid, u in users.items():
        if u.get("wait_voice"):
            await bot.send_voice(uid, message.voice.file_id)
            clear_wait(u)
            await message.answer("✅ Голос отправлен")
            return


# =====================
# ЗАПУСК
# =====================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
