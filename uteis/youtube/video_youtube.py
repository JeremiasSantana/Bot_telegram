import asyncio
import os

import yt_dlp
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_ytvideo = Router(name='Router_videoyt')


def config_yt(pesquisa: str) -> str:
    buscar_pesquisa = f'ytsearch1:{pesquisa}'
    opts_dlp = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '/home/jeremias/Documentos/pasta_de_projetos/jota_bot/videos_bot/yt_%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'continuedl': True,
        'quiet': True,
        'max_filesize': 50 * 1024 * 1024
    }

    with yt_dlp.YoutubeDL(opts_dlp) as youtube:
        info_video = youtube.extract_info(buscar_pesquisa, download=True)
        pega_resultado1 = info_video['entries'][0]
        return youtube.prepare_filename(pega_resultado1)



@router_ytvideo.message(Command('ytvideo'))
async def baixar_video(menssagem: types.Message):

    parte_pesquisa = menssagem.text.split(" ", 1)

    if len(parte_pesquisa) < 2:
        await menssagem.reply(
            '❎ ​Digite o comando seguido do video que você quer que o robô busque!!\n'\
            'EXP.: /ytvideo ze vaqueiro'
        )
        return

    pesquisa = parte_pesquisa[1].strip()
    status_espera = await menssagem.reply(f'🔍 So um momento, ja estou procurando por "{pesquisa}"')
    caminho_arquivo = None

    try:
        caminho_arquivo = await asyncio.to_thread(config_yt, pesquisa)
        video = FSInputFile(caminho_arquivo)

        await menssagem.reply_video(
            video=video,
            caption="🎞️​ Aqui está seu video!! Quando quiser mais, estarei a sua disposição🫡​",
            parse_mode="Markdown"
        )

    except Exception as erro:
        erro_str = str(erro).lower()

        if 'filesize' in erro_str:
            await menssagem.reply(f'✖️​ Infelizmente não tem como eu te fornecer o "{pesquisa}"!! O vídeo tem mais MB do que o telegram permite(50MB)!!')
        else:
            await menssagem.reply('❎​ Não consegui baixar o video! Tente novamente com outros termos')
        print(f"Erro youtube: {erro}")
    finally:
        await status_espera.delete()
        if caminho_arquivo and os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)