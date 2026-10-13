import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from uteis.menu.config_menu import router_menu
from uteis.ytvideo.video_youtube import router_yt_video

load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")
bot = Bot(token=f"{TOKEN}")
dp_bot = Dispatcher()



async def main():
    print("Bot rodando...")
    dp_bot.include_routers(
        router_menu,
        router_yt_video
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp_bot.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
