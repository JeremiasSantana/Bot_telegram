import yt_dlp
import asyncio
import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_yt_video = Router(name='yt_video')


def config_youtube(pesquisa):
    procurar_video = f"ytsearch1:{pesquisa}".strip()

    config_ydl = {

        'fromat': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '/home/jeremias/Documentos/pasta_de_projetos/jota_bot/videos_bot/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'continuedl': True,
        'merge_output_format': 'mp4',
        'ignoreerros': True,
        'maxsize': 50 * 1024 * 1024
    }

    with yt_dlp.YoutubeDL(config_ydl) as youtube:
        info = youtube.extract_info(procurar_video, download=True)
        primeiro_resultado = info['entries'][0]
        return youtube.prepare_filename(primeiro_resultado)


@router_yt_video.message(Command('ytvideo'))
async def baixar_videoyt(menssagem: types.Message):
    parte_procura = menssagem.text.split(' ', 1)

    if len(parte_procura) < 2:
        await menssagem.reply(
            "Digite o comando texto do video que deseja pegar.\n" \
            "Exemplo: /ytvideo vidigal"
        )
        return

    pesquisar_parte = parte_procura[1].strip()
    status_pesquisa = await menssagem.reply(f"Pesquisando por '{pesquisar_parte}'...")

    caminho_arquivo = None

    try:
        caminho_arquivo = await asyncio.to_thread(config_youtube, pesquisar_parte)
        video = FSInputFile(caminho_arquivo)

        await menssagem.reply_video(
            video=video,
            caption="Aqui está seu vídeo!!",
            parse_mode='Markdown'
        )
    except Exception as erro:
        erro_str = str(erro)

        if "filesize" in erro_str:
            await menssagem.reply("O video atinge mais MB do que o telegram aceita(50MB)")

        else:
            await menssagem.reply("Não foi possivel baixar o video. Tente novamente com outros termos")


    finally:
        status_pesquisa.delete()

        if caminho_arquivo and os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

    
