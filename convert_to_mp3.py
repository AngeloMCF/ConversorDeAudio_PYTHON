import os
from datetime import datetime
import time

from pydub import AudioSegment, effects


def limpa_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


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


def criar_diretorio_converteded(dir_path:str, dir_name:str) -> None:
    if dir_name not in os.listdir(dir_path):
        os.mkdir( os.path.join(dir_path, dir_name)) 


def time_formated(tempo: time.localtime = time.localtime() ):
    print(f'{tempo.tm_hour}h {tempo.tm_min} min {tempo.tm_sec} sec')


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
    tempo_formatado:str = '0:00:00.000000' #f'{tempo.hour} : {tempo.minute} {tempo.second}  {tempo.microsecond}'
    mensagem =f"| Execução: {execucao} | Run time: {_time_stamp if _time_stamp.days>= 0 else tempo_formatado} | Erros: {qnt_erro} |"
    print(f'{caratere*len(mensagem)}')
    print(mensagem)
    print(f'{caratere*len(mensagem)}')


def log_to_file(erro:str, texto:str, file_name:str = 'logs.txt'):
    with open (file_name, 'w+') as _log_file:
        m:str =f'Erro durante execucao: "{texto}", erro: {erro}' 
        _log_file.write(m)


def exportar_mp3(lista:list, dir_music:str, dir_eport_path:str,
                equalizar_audio: bool = True, 
                remover_silencio_bordas: bool = False,
                renomear_arquivo_final: bool = True,
                arquivo_final_inicio: str = '_converted_'
                ):
    qnt: int = len(lista)
    cc: int= 0
    cc_erros: int = cc
    start_time = datetime.today()

    for file in lista:
        _infos(cc + 1, start_time, cc_erros)
        show_message(cc, qnt, file)
        try:
            _mp3file_path = os.path.join(dir_music, file)
            _extension:str = file[-3::]
            # mp3: AudioSegment = AudioSegment.from_mp3(_mp3file_path)
            mp3: AudioSegment = AudioSegment.from_file(_mp3file_path, _extension)
            print('\tArquivo extraído.')
            
            if equalizar_audio:
                print('\tIniciando normalizção.')
                mp3 = effects.normalize(mp3)
                print('\tArquivo normalizado.')
            
            if remover_silencio_bordas:
                print('\tRemovendo silêncio das bordas.')
                mp3 = effects.strip_silence(mp3)
                print('\tSilêncio removido.')
            
            print('\tExportando aquivo.')

            nome_arquivo = f'{arquivo_final_inicio}{file[:-3]}.mp3' if renomear_arquivo_final else f'{file[:-3]}.mp3' 
            caminho_arquivo_final:str = f'{dir_eport_path}/{nome_arquivo}'
            mp3.export(caminho_arquivo_final, format='mp3')
            print('\tArquivo exportando.')
        except Exception as e:
            error_message:str = f'exec:{cc}'
            log_to_file(e, error_message)
            cc_erros += 1      
        
        cc +=1
        limpa_tela()
    
    _infos(cc, start_time, cc_erros)

    show_message(cc, qnt)
 

def run():
    limpa_tela()

    diretorio_raiz:str = 'assets'
    diretorio_musicas:str = os.path.join(diretorio_raiz, '_samples')
    diretorio_musicas_convertidas:str = '_converted'

    criar_diretorio_converteded(diretorio_raiz, diretorio_musicas_convertidas)
    
    arquivos:list =  listar_diretorio_por_tipo_arquivo(diretorio_musicas, ['.mp4', '.mp3'])
    
    exportar_mp3(arquivos,diretorio_musicas, os.path.join(diretorio_raiz, diretorio_musicas_convertidas), renomear_arquivo_final= False)

if __name__ == '__main__':
    run()

