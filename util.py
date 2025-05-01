import os
from datetime import datetime

from default_config import diretorio_musicas_coverter,  diretorio_musicas_covertidas
from default_config import destino_video, destino_audio, arquivo_links_baixar_youtube

def criar_diretorio_converteded(dir_path:str, dir_name:str) -> None:
    if dir_name not in os.listdir(dir_path):
        os.mkdir( os.path.join(dir_path, dir_name)) 

def create_dir(path:str) -> None:

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e :
            print(f'error create_dir : {e}' )

def setup() -> None:
    
    cwd:str = os.getcwd()

    create_dir(os.path.join(cwd, 'assets'))
    create_dir(os.path.join(cwd, 'logs'))
    create_dir(os.path.join(cwd, diretorio_musicas_coverter.replace('./', '')))
    create_dir(os.path.join(cwd, diretorio_musicas_covertidas.replace('./', '')))
    create_dir(os.path.join(cwd, destino_video.replace('./', '')))
    create_dir(os.path.join(cwd, destino_audio.replace('./', '')))
    create_dir(os.path.join(cwd, arquivo_links_baixar_youtube.replace('./', '')))


def clean_scream() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def log_to_file(erro:str, texto:str, file_name:str = f"{str(datetime.now())[:19].replace(':', '-').replace(' ', '-')}-logs.txt", crititca:bool = True):

    with open (os.path.join('logs', file_name), 'a') as _log_file:
        m:str = f'Erro durante execucao: "{texto}", erro: {erro}' if crititca else texto
        _log_file.write(m)


if __name__ == '__main__':
    clean_scream()
    setup()
    print('Setup Done!')
