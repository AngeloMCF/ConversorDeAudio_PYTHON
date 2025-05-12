import sys
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages" :
        ["os"], "includes" : ["tkinter", "pytubefix", "pydub", "audioop"]
}

# GUI applications require a different base on Windows (the default is fora console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ConverterEBaixarAudio",
    version="0.1",
    description="Baixa e converte arquivos de audio",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui.py", base=base)]
)

# terminal
# python ./setup.py build