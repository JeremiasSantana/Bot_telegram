import asyncio
import os

import yt_dlp
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_ytmusic =  Router(name="Router_youtube_music")



def config_audio(pesquisa: str):
    busca_pesquisa = f'ytsearch1:{pesquisa}'
    audio_dlp = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': '/home/jeremias/Documentos/pasta_de_projetos/jota_bot/audios_bot/yt_%(title)s.%(ext)s',
        'filesize': 50 * 1024 * 1024,
        'retries': 5,
        'extractor_retries': 5,
        'quiet': True,
        'noplaylist': True

    }

    with yt_dlp.YoutubeDL(audio_dlp) as youtube_music:
        info_music = youtube_music.extract_info(busca_pesquisa, download=True)
        pegar_result1 = info_music['entries'][0]

        return youtube_music.prepare_filename(pegar_result1)



@router_ytmusic.message(Command('ytmusica'))
async def yt_musica(menssagem: types.Message):
    comando = menssagem.text.split(" ", 1)

    if len(comando) < 2:
        await menssagem.reply(
            "Digite o comando seguido do audio que deseja pegar do youtube.\n" \
            "Ex.: /ytmusica pcn boladão paranga"
        )
        return

    parte_pesquisa = comando[1].strip()
    status = await menssagem.reply(f'Procurando por "{parte_pesquisa}"...')

    pacote_musica = None

    try:
        pacote_musica = await asyncio.to_thread(config_audio, parte_pesquisa)
        musica = FSInputFile(pacote_musica)

        await menssagem.reply_audio(
            audio=musica,
            caption='Aqui está sua música! Se divirta e até mais'
        )

    except Exception as erro:
        erro_str = str(erro)

        if "filesize" in erro_str:
            print(erro)
            await menssagem.reply(f'Não consegui baixar {parte_pesquisa}!!! O arquivo excede o limiete do telegram(50MB)')
            return
        else:
            print(erro)
            await menssagem.reply(f"Não consegui baixar {parte_pesquisa}!! Tente novamente usando outras vertentes")
            return

    finally:
        await status.delete()

        if pacote_musica and os.path.exists(pacote_musica):
            os.remove(pacote_musica)
        
