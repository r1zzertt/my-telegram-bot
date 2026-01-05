import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, ADMIN_ID
from nodes import send_node
from state import reset_user, get_user_state, clear_wait
from inventory import inventory_text
from voices import save_voice, get_voice

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =====================
# /start
# =====================
@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        reset_user(message.from_user.id)
        await send_node(message, "start")


# =====================
# КНОПКИ
# =====================
@dp.callback_query()
async def callbacks(callback: CallbackQuery):
    user = get_user_state(callback.from_user.id)

    # 🎒 Инвентарь
    if callback.data == "inventory":
        await callback.answer()
        await callback.message.answer(
            inventory_text(user)
        )
        return

    # 🔀 Переход по сценам
    if callback.data.startswith("node:"):
        node_id = callback.data.split(":")[1]
        await callback.message.delete()
        await send_node(callback.message, node_id)


# =====================
# СОХРАНЕНИЕ ГОЛОСА
# =====================
@dp.message()
async def save_voice_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text and message.text.startswith("/save"):
        key = message.text.split(" ", 1)[1]
        admin = get_user_state(ADMIN_ID)
        admin["wait_voice"] = key
        await message.answer(f"🎙 Жду голос для ключа: {key}")


# =====================
# ГОЛОСОВЫЕ
# =====================
@dp.message()
async def voice_handler(message: Message):
    if not message.voice:
        return

    user = get_user_state(message.from_user.id)

    # 🔴 ЕСЛИ ЭТО АДМИН
    if message.from_user.id == ADMIN_ID:
        admin = get_user_state(ADMIN_ID)

        # 💾 сохранение голоса
        if admin.get("wait_voice"):
            save_voice(admin["wait_voice"], message.voice.file_id)
            clear_wait(admin)
            await message.answer("💾 Голос сохранён")
            return

        # 🎤 живой голос игроку
        for uid, u in list(getattr(__import__("state"), "users").items()):
            if u.get("wait_voice"):
                await bot.send_voice(
                    uid,
                    message.voice.file_id
                )
                clear_wait(u)
                await message.answer("✅ Голос отправлен ей")
                return


# =====================
# ЗАПУСК
# =====================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
