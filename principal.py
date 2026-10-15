import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from uteis.menu.config_menu import router_menu
from uteis.youtube.video_youtube import router_ytvideo
from uteis.youtube.musica_boy import router_ytmusic

load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")
bot = Bot(token=f"{TOKEN}")
dp_bot = Dispatcher()



async def main():
    print("Bot rodando...")
    dp_bot.include_routers(
        router_menu,
        router_ytvideo,
        router_ytmusic
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp_bot.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
