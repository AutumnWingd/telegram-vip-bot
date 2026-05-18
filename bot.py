import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

bot = Bot(token=TOKEN)
dp = Dispatcher()


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💎 开通会员", callback_data="vip")],
        [InlineKeyboardButton(text="👤 我的会员", callback_data="me")],
    ]
)


@dp.message(F.text == "/start")
async def start(message: Message):

    photo = FSInputFile("image.jpg")

    await message.answer_photo(
        photo=photo,
        caption="""
🏠 欢迎来到会员商店

💎 VIP 月卡
🔥 SVIP 月卡

付款后联系管理员。
""",
        reply_markup=main_keyboard
    )


@dp.callback_query(F.data == "vip")
async def vip(callback: CallbackQuery):

    text = """
💎 VIP 月卡：88

🔥 SVIP 月卡：188

付款方式：

支付宝：
你的支付宝

USDT(TRC20)：
你的USDT地址

银行卡：
你的银行卡

付款后联系管理员。
"""

    await callback.message.answer(text)


@dp.callback_query(F.data == "me")
async def me(callback: CallbackQuery):
    await callback.message.answer("你当前暂无会员")


async def health(request):
    return web.Response(text="Bot is running")


async def main():
    print("Bot running...")

    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
