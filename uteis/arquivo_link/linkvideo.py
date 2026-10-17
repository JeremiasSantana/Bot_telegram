import asyncio
import os

import yt_dlp
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_video_link =  Router(name='link_videos')


def config_link(link: str):
    
    ydl_config = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '/home/jeremias/Documentos/pasta_de_projetos/jota_bot/videos_bot/yt_%(id)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True,
        'continuedl': True,
        'noplaylist': True

    }

    with yt_dlp.YoutubeDL(ydl_config) as ytlink_video:
        infos = ytlink_video.extract_info(link, download=True)
        return ytlink_video.prepare_filename(infos)


@router_video_link.message(Command('videolink'))
async def baixar_videolink(message: types.Message):
    parte_comando = message.text.split(" ", 1)

    if len(parte_comando) < 2:
        await message.reply(
            "Digite o comando seguido do link.\n" \
            "Ex.: /linkvideo https//[...]"
        )
        return

    link = parte_comando[1].strip()
    status = await message.reply("So um momento, estou indo atrás do seu video...")
    fragmento_video = None

    try:

        if not link.startswith("http"):
            await message.reply("Não consegui buscar o seu vídeo porque esse link é invalido")
            return

        fragmento_video = await asyncio.to_thread(config_link, link)
        video = FSInputFile(fragmento_video)

        await message.reply_video(
            video=video,
            caption="Aqui está seu video!! Se preicsa de algo, estou a disposição"
        )

    except Exception as erro:
        erro_str = str(erro)

        if 'filesize' in erro_str:
            await message.reply("Não foi possivel baixar seu video porque ele excede o limite de mb que o telegram permite (50MB)")
            return

        else:
            print(erro)
            await message.reply("Não foi possivel baixar o video atraves de seu link")
            return

    finally:
        await status.delete()

        if fragmento_video and os.path.exists(fragmento_video):
            os.remove(fragmento_video)
