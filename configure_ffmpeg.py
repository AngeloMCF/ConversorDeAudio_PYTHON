import os
import sys
from zipfile import ZipFile

def extract_zipfile(path) -> None:
    with ZipFile(path, 'r') as zip:
        zip.extractall()


def create_bat(bin_path) -> None:
    script :str = f'@echo off \nsetx ffmpeg "{bin_path}"'

    try:
        with open ('bat_ffmpeg.bat', 'w', encoding='utf-8') as file:
            file.write(script)

        script :str = f'@echo off \nsetx ffmpeg "{bin_path}" /M'
        with open ('bat_ffmpeg_run_as_admin.bat', 'w', encoding='utf-8') as file:
            file.write(script)

    except Exception as e:
        pass


def delete_bat_files() -> None:
    bat_list:list = [i for i in os.listdir(os.getcwd()) if os.path.isfile(i) and '.bat' in i]
    for file in bat_list:
        os.remove(file)


def run() -> None:

    ffmpeg_file_zip_name:str = [i for i in os.listdir(os.getcwd()) if os.path.isfile(i) and 'ffmpeg' in i and '.zip'  in i][0]

    if type(ffmpeg_file_zip_name) == str:
        extract_zipfile(ffmpeg_file_zip_name)

        name = os.path.join(os.getcwd(), ffmpeg_file_zip_name.replace('.zip', ''), 'bin')

        if os.path.exists(name):
            create_bat(name)

        try:
            os.system('bat_ffmpeg.bat')

        except Exception as e:
            print(f'erro nao tratado, execute bat {e}')

# NOTE IF THIS DIDN'T WORK, 
# TRY ADD THE FULL PATH 
#   '~/ffmpeg-2024-11-21-git-f298507323-essentials_build\bin' 
# TO PATH ON WINDOWS ENV VARIABLES 

if __name__ == '__main__':
    run()
    # delete_bat_files()

 