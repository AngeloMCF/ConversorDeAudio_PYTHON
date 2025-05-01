import os
from datetime import datetime
import util

from default_config import diretorio_musicas_covertidas, diretorio_musicas_coverter, lista_formatos_aceitos

from pydub import AudioSegment, effects

def show_message(total_atual: int, total_max:int, file: str =None) -> None:
    print(f'Convertidos {total_atual} de {total_max} : {(total_atual/total_max)*100:.2f}%')
    if file: print(f'Iniciando conversão de: {file}')


def listar_diretorio(diname:str, file_type:str = None) -> list[str]:
    _list: list = [_file for _file in os.listdir(diname) if os.path.isfile(os.path.join(diname,_file))] if file_type else os.listdir(diname)
    return _list


def listar_diretorio_trava(diname:str, file_type:str = None, quantidade_arquivos: int = 5) -> list[str]:
    _list: list = [_file for _file in os.listdir(diname)[0:quantidade_arquivos] if _file.endswith(file_type) ] if file_type else os.listdir(diname)
    return _list


def listar_diretorio_por_tipo_arquivo(diname:str, file_types:list = None) -> list[str]:
    _list: list = []
    for _file in [_file for _file in os.listdir(diname) if os.path.isfile(os.path.join(diname,_file))]:            
        for _type in file_types:
            if _type in _file: _list.append(_file)

    return _list

def _infos(execucao: int, tempo: datetime, qnt_erro: int = 0, _time: int = 0, espaco:int = 10):
    """ Função para exibir informações das execuções. 

        | Execução: {execucao} ({_time_txt}) | Run time: {now(tempo)} | Erros: {qnt_erro} |
    """
    
    if (_time == 0): # Tempo que será executado a próxima atualização de valores
        _time_txt = '0'

    elif (_time <= 60): # seconds
        _time_txt = f'{_time} s'

    elif(_time <3600): # minutes
        if ((_time % 60) ==0): # minto interio
            _time = _time/60
            _time_txt = f'{_time:.0f} min'
        else: # minto com segundos
            _seconds = _time % 60 
            _time = _time/60 
            _time_txt = f'{_time:.0f}:{_seconds} min'

    else: # Horas
        _seconds = (_time % 3600)/60 
        _time = _time/3600 
        _time_txt = f'{_time:.0f}:{_seconds:.0f} h'

    caratere = '-'
    _time_stamp = datetime.now() - tempo
    tempo_formatado:str = '0:00:00.000000' 
    mensagem =f"| Execução: {execucao} | Run time: {_time_stamp if _time_stamp.days >= 0 else tempo_formatado} | Erros: {qnt_erro} |"
    print(f'{caratere*len(mensagem)}')
    print(mensagem)
    print(f'{caratere*len(mensagem)}')


def export_mp3_list(lista:list, dir_music:str, dir_eport_path:str,
                equalize_audio: bool = True, 
                remove_silence_edges: bool = False,
                rename_final_file: bool = True,
                arquivo_final_inicio: str = '_converted_'
                ):
    qnt: int = len(lista)
    cc: int= 0
    cc_erros: int = cc
    start_time = datetime.today()

    log_file_name:str = f"{str(datetime.now())[:19].replace(':', '-').replace(' ', '-')}-logs.txt"

    for file in lista:
        _infos(cc + 1, start_time, cc_erros)
        show_message(cc, qnt, file)
    
        try:
            _mp3file_path = os.path.join(dir_music, file)

            file_name = f'{arquivo_final_inicio}{file[:-3]}.mp3' if rename_final_file else f'{file[:-3]}.mp3' 
            file_name = file_name.replace('..', '.')
            caminho_arquivo_final:str = os.path.join(dir_eport_path, file_name)

            convert_mp3(_mp3file_path, caminho_arquivo_final, file, equalize_audio = equalize_audio, remove_silence_edges= remove_silence_edges)
            util.log_to_file('', f'Info - exportado "{file_name}"', file_name=log_file_name, crititca=False)
            
            cc += 1

        except Exception as e:
            error_message:str = f'exec:{cc}'
            util.log_to_file(e, error_message, file_name=log_file_name)
            cc_erros += 1      
        
        util.clean_scream()
    
    _infos(cc, start_time, cc_erros)

    show_message(cc, qnt)

    if os.path.exists(f'logs/{log_file_name}'):
        print(f'Arquivo de logs em: "./logs/{log_file_name}"')

def convert_mp3(input_path:str, output_path:str, file:str, 
                equalize_audio: bool = False, 
                remove_silence_edges: bool = False) -> None:

    try:
        input_path = input_path.replace('./', '').replace('/', '\\')
        output_path = output_path.replace('./', '').replace('/', '\\')

        file_extension:str = file[-3::]
        file_name:str = file.replace(file_extension, '').replace('.', '')
        cwd:str= os.getcwd()
        caminho:str = os.path.join(cwd, input_path, file)
        caminho_arquivo_final:str = os.path.join(cwd, output_path,file_name + '.mp3' )

        print('\tIniciando extracao.')
        mp3: AudioSegment = AudioSegment.from_file(caminho, file_extension)
        print('\tArquivo extraido.')

        if equalize_audio:
            print('\tIniciando normalizacao.')
            mp3 = effects.normalize(mp3)
            print('\tArquivo normalizado.')
            
        if remove_silence_edges:
            print('\tRemovendo silencio das bordas.')
            mp3 = effects.strip_silence(mp3)
            print('\tSilencio removido.')
        
        print('\tExportando aquivo.')
        mp3.export(caminho_arquivo_final, format='mp3')
        print('\tArquivo exportado.\n')

    except Exception as e:
        print(f'erro convert_mp3: {e}')
 

def run():
    util.setup()
    util.clean_scream()

    diretorio_musicas:str = diretorio_musicas_coverter
    diretorio_musicas_convertidas:str = diretorio_musicas_covertidas

    arquivos:list = listar_diretorio_por_tipo_arquivo(diretorio_musicas, lista_formatos_aceitos)

    print(len(arquivos) > 0, len(arquivos), arquivos )

    if len(arquivos) > 0: 
        export_mp3_list(arquivos,diretorio_musicas,diretorio_musicas_convertidas, rename_final_file= False)
    else:
        print(f'Arquivo vazio: "{diretorio_musicas}"')

@NotImplementedError
def __force():

    file_in  = r'' # full path 
    file_out = r'' # full path 

    try:
        mp3: AudioSegment = AudioSegment.from_file(file_in, 'm4a')
        print('\tArquivo extraído.')
                
        print('\tExportando aquivo.')

        mp3.export(file_out, format='mp3')
        print('\tArquivo exportado.')

    except Exception as e:
        print(e)

    try:
        os.remove(file_in)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    run()
    # __force()

