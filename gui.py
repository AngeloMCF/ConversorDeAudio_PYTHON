import tkinter as tk
from tkinter import ttk, messagebox

# import pygame 
# pygame.mixer.init()

import util

import convert_to_mp3 as conversor
import download_from_youtube as dfy


def baixar_video_audio():
    url = url_entry.get()
    if url:
        try:
            dfy.download(url)
            messagebox.showinfo("Sucesso", "Download de vídeo e áudio concluído.")
        except Exception as e:
            util.log_to_file(e, 'gui_baixar_video_audio')
            messagebox.showerror("Erro", "URL inválida.")
            return

    else:
        messagebox.showerror("Erro", "URL não pode estar vazia.")

def baixar_audio_mp3():
    url = url_entry.get()
    if url:
        try:
            dfy.download_mp3(url)
            messagebox.showinfo("Sucesso", "Download de áudio MP3 concluído.")
        except Exception as e:
            util.log_to_file(e, 'gui_baixar_audio_mp3')
            messagebox.showerror("Erro", "URL inválida.")
            return

    else:
        messagebox.showerror("Erro", "URL não pode estar vazia.")

def recortar_audio():
    try:
        arquivos = conversor.lista_arquivos()
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Diretório '{ conversor.diretorio_musicas_covertidas}' não encontrado.")
        return

    if not arquivos:
        messagebox.showinfo("Nenhum arquivo", "Nenhum arquivo de áudio encontrado.")
        return

    # Criar nova janela para seleção
    seletor = tk.Toplevel(root)
    seletor.title("Selecionar arquivo de áudio")
    seletor.geometry("400x300")
    seletor.configure(bg="#2e2e2e")

    ttk.Label(seletor, text="Selecione um arquivo para recortar:", style="TLabel").pack(pady=10)

    lista = tk.Listbox(seletor, bg="#3e3e3e", fg="#ffffff", selectbackground="#888", activestyle="none")
    for idx, nome in enumerate(arquivos, start=1):
        lista.insert(tk.END, f"[{idx}] {nome}")
    lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def confirmar():
        selecionado = lista.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return
        idx = selecionado[0]
        arquivo_escolhido = arquivos[idx]
        seletor.destroy()

        # Nova janela para entrada de segundos
        entrada = tk.Toplevel(root)
        entrada.title("Definir trecho do áudio")
        entrada.geometry("350x300")
        entrada.configure(bg="#2e2e2e")

        ttk.Label(entrada, text=f"Arquivo: {arquivo_escolhido}", style="TLabel").pack(pady=(10, 5))

        ttk.Label(entrada, text="Digite o segundo inicial:", style="TLabel").pack()
        inicio_entry = ttk.Entry(entrada)
        inicio_entry.pack(pady=5)

        ttk.Label(entrada, text="Digite o segundo final:", style="TLabel").pack()
        fim_entry = ttk.Entry(entrada)
        fim_entry.pack(pady=5)

        # caminho_audio = os.path.join(conversor.diretorio_musicas_covertidas, arquivo_escolhido)

        # def play_audio():
        #     try:
        #         pygame.mixer.music.load(caminho_audio)
        #         pygame.mixer.music.play()
        #     except Exception as e:
        #         messagebox.showerror("Erro ao reproduzir", str(e))

        # def stop_audio():
        #     pygame.mixer.music.stop()

        # ttk.Button(entrada, text="▶️ Play", style="Dark.TButton", command=play_audio).pack(pady=(10, 2))
        # ttk.Button(entrada, text="⏹ Stop", style="Dark.TButton", command=stop_audio).pack(pady=(0, 10))

        def cortar():
            try:
                inicio = int(inicio_entry.get())
                fim = int(fim_entry.get())
                if inicio >= fim:
                    raise ValueError("O tempo inicial deve ser menor que o final.")
                entrada.destroy()
                # pygame.mixer.music.stop()
                conversor.cut_audio_segment(arquivo_escolhido, inicio, fim)
                messagebox.showinfo("Sucesso", f"Áudio '{arquivo_escolhido}' recortado com sucesso.")
            except ValueError as e:
                messagebox.showerror("Erro", f"Entrada inválida: {e}")

        ttk.Button(entrada, text="Recortar", style="Dark.TButton", command=cortar).pack(pady=10)

    ttk.Button(seletor, text="Confirmar", style="Dark.TButton", command=confirmar).pack(pady=10)


def encerrar_execucao():
    root.quit()

# Setup da interface
util.setup()
root = tk.Tk()
root.title("Downloader YouTube")
root.geometry("500x300")
root.configure(bg="#2e2e2e")

# Estilo do ttk
style = ttk.Style(root)
style.theme_use("default")

# Estilo base dos botões
style.configure("Dark.TButton",
    background="#444",
    foreground="#fff",
    font=("Segoe UI", 10),
    padding=6,
    borderwidth=1,
    focusthickness=3,
    focuscolor='none'
)

# Estilo ao passar o mouse (estado 'active')
style.map("Dark.TButton",
    background=[('active', '#ddd')],
    foreground=[('active', '#000')],
)

# Estilo para label e entry
style.configure("TLabel", background="#2e2e2e", foreground="#fff", font=("Segoe UI", 10))
style.configure("TEntry", fieldbackground="#3e3e3e", foreground="#fff")

# Widgets
ttk.Label(root, text="Insira a URL do vídeo:").pack(pady=(20, 5))
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

ttk.Button(root, text="[1] Baixar vídeo (mp4) e áudio (m4a)", style="Dark.TButton", command=baixar_video_audio).pack(pady=5)
ttk.Button(root, text="[2] Recortar áudio", style="Dark.TButton", command=recortar_audio).pack(pady=5)
ttk.Button(root, text="[3] Baixar áudio (mp3)", style="Dark.TButton", command=baixar_audio_mp3).pack(pady=5)
ttk.Button(root, text="[0] Encerrar execução", style="Dark.TButton", command=encerrar_execucao).pack(pady=(20, 10))

root.mainloop()
