import asyncio
import os

import yt_dlp
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_audio = Router(name='router audio')



def config_audio(link: str):
    config_link = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'max_falisize': 50 * 1024 * 1024,
        'outtmpl': '/home/jeremias/Documentos/pasta_de_projetos/jota_bot/audios_bot/%(title)s.%(ext)s',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }]

    }

    with yt_dlp.YoutubeDL(config_link) as link_audio:
        info_arquivo = link_audio.extract_info(link, download=True)
        return link_audio.prepare_filename(info_arquivo)


@router_audio.message(Command('audiolink'))
async def baixar_audio(menssagem: types.Message):
    parte_comando =  menssagem.text.split(" ", 1)

    if len(parte_comando) < 2:
        await menssagem.reply(
            'Digite o comando seguido do link que deseja extrair o aúdio.\n' \
            'Ex.: /linkaudio http[...]'
        )
        return

    link = parte_comando[1].strip()

    if not link.startswith('http'):
        await menssagem.reply('Impossivél extrair aúdio.\n' \
        'Digite um link válido')
        return

    status = await menssagem.reply("Ja estou trabalhando na busca da extração do seu aúdio. So um momento...")
    fragmento_arquivo = None

    try:
        fragmento_arquivo = await asyncio.to_thread(config_audio, link)
        audio = FSInputFile(fragmento_arquivo)

        await menssagem.reply_audio(
            audio=audio,
            caption='Aqui está o teu aúdio!! Se precisar de mias alguma coisa, estou ao teu dispor!!!'
        )

    except Exception as erro:
        erro_str = str(erro)

        if 'filesize' in erro_str:
            await menssagem.reply("Não foi possivel extrair o aúdio porque ele excede o tamanho de mb que o telegram permite(50MB)!!")
            return

        else:
            await menssagem.reply("Não consegui extrair teu aúdio pelo teu link. Tente novamente ou verifique se o link está correto!!!")
            return

    finally:
        status.delete()
        if fragmento_arquivo and os.path.exists(fragmento_arquivo):
            os.remove(fragmento_arquivo)