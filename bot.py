import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from nodes import send_node
from state import reset_user, get_user_state
from inventory import inventory_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        reset_user(message.from_user.id)
        await send_node(message, "start")


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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
