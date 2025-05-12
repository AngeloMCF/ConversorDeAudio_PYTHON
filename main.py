import util

import convert_to_mp3 as conversor
import download_from_youtube as dfy


def run() -> None:
    util.setup()
    choice: int = 0

    srt_choice:str ="\n\nOpcoes disponiveis: \n" \
    "\t[0] Encerrar execucao \n" \
    "\t[1] Baixar video (mp4) e audio (m4a) \n" \
    "\t[2] Recortar audio \n" \
    "\t[3] Baixar audio (mp3) \n" \
    "Digite a opcao escolhida: "

    while True:

        try:
            choice = int(input(srt_choice))

            if choice not in(0,1,2,3):
                print('!!! Opcao Invalida !!!')

            elif choice == 0:
                print('Encerrando execucao')
                break

            elif choice == 1:
                url:str = input('Insira a url do video: ')

                try:
                    dfy.download(url)
                except Exception as e:
                    print('Erro.\nVerifique se a url e valida.')

            elif choice == 2:
                conversor._cut_audio_segment()

            elif choice == 3:
                url:str = input('Insira a url do video: ')
                try:
                    dfy.download_mp3(url)
                except Exception as e:
                    print('Erro.\nVerifique se a url e valida.')

        except Exception as e:
            print(e)
            print('!!! Opcao Invalida !!!')

            pass

        choice = 0


if __name__ == '__main__':
    util.clean_scream()
    run()

