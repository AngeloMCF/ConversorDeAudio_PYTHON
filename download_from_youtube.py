from pytubefix import YouTube
from pytubefix.cli import on_progress

import os

from default_config import destino_video, destino_audio, diretorio_musicas_covertidas
import util

from convert_to_mp3 import convert_mp3

def download(url:str) -> None :

    yt:YouTube = YouTube(url, on_progress_callback=on_progress)
    
    download_mp4(yt)
    download_m4a(yt)
    
def download_m4a(youtube: YouTube) -> None :
    try:
        youtube_audio = youtube.streams.get_audio_only()
        youtube_audio.download(output_path=destino_audio)

    except Exception as e:
        util.log_to_file(e, 'download_m4a')

def download_mp3(url:str):
    yt:YouTube = YouTube(url, on_progress_callback=on_progress)
    yt.title = normalize_name(yt.title)
    
    file: str = yt.title + '.m4a'

    download_m4a(yt)

    convert_mp3(destino_audio, diretorio_musicas_covertidas, file)

    try:
        remove_file_path:str = os.path.join(destino_audio, file) 
        os.remove(remove_file_path)
    except Exception as e:
        util.log_to_file(e, 'download_mp3 -  os.remove(remove_file_path)')


def download_mp4(youtube: YouTube) -> None :
    try:
        youtube_video = youtube.streams.get_highest_resolution()
        youtube_video.download(output_path=destino_video, filename=normalize_name(youtube_video.title) + '.mp4')
    except Exception as e:
        util.log_to_file(e, 'download_mp4')


def normalize_name(string:str) -> str:
    return util.remove_reserved_char(string)

def baixar_lista() -> None:
    aqruivo_urls = r'.\assets\lista_link_youtube\lista.txt'

    lista_url:list = []
    with open(aqruivo_urls, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.strip()[0] == '#':
                continue
            lista_url.append(linha.strip())

    if (not lista_url or len(lista_url) <= 0):
        print('Lista vazia')
        return

    cc:int = 0
    quantidade_itens:int = len(lista_url)
    print(f'URLs a processar: {quantidade_itens}')
    for url in lista_url:
        util.clean_scream()
        try:
            print(f'Processando url: {cc +1}/{quantidade_itens} \n' )
            download_mp3(url)
            print()
        except Exception as e:
            util.log_to_file(e, f'baixar_lista')
        cc += 1

def run():
    util.setup()
    util.clean_scream()

    url:str = 'https://www.youtube.com/watch?v=_ovdm2yX4MA'

    download(url)
    # download_mp3(url)
    

if __name__ == '__main__':
    run()
