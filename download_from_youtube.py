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
    
    print(yt.title)

    
def download_m4a(youtube: YouTube) -> None :
    try:
        youtube_audio = youtube.streams.get_audio_only()
        youtube_audio.download(output_path=destino_audio)
        print(f'arquivo salvo em: "{destino_audio}\n"')

    except Exception as e:
        print(f'erro durante: download_m4a; url:{youtube.url}')


def download_mp3(url):
    yt:YouTube = YouTube(url, on_progress_callback=on_progress)
    file: str = yt.title + '.m4a'
    print(file)
    download_m4a(yt)

    convert_mp3(destino_audio, diretorio_musicas_covertidas, file)

    try:
        remove_file_path:str = os.path.join(destino_audio, file) 
        os.remove(remove_file_path)
    except Exception as e:
        print(e)

def download_mp4(youtube: YouTube) -> None :
    try:
        youtube_video = youtube.streams.get_highest_resolution()
        youtube_video.download(output_path=destino_video)

    except Exception as e:
        print(f'erro durante: download_mp4; url:{youtube.url}')


def run():
    util.setup()
    util.clean_scream()

    url:str = 'https://www.youtube.com/watch?v=_ovdm2yX4MA'

    download(url)
    download_mp3(url)
    

if __name__ == '__main__':
    run()
