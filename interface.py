import tkinter as tk
from tkinter import filedialog
import captions_extractor as ce

def selecionar_arquivo(entrada_arquivo):
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo"
    )
    if arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, arquivo)

def selecionar_diretorio(entrada_diretorio):
    diretorio = filedialog.askdirectory(
        title="Selecione o diretório de salvamento"
    )
    if diretorio:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, diretorio)

def executar(entrada_arquivo, entrada_diretorio):
    arquivo = entrada_arquivo.get()
    diretorio = entrada_diretorio.get()

    print("Arquivo selecionado:", arquivo)
    print("Diretório de saída:", diretorio)
    ce.main(video_fpath=arquivo, caption_dpath=diretorio, caption_language="pt")

def create_interface():
    root = tk.Tk()
    root.title("Selecionar Arquivo e Diretório")
    root.geometry("600x180")

    # Arquivo de entrada
    tk.Label(root, text="Arquivo de entrada:").pack(anchor="w", padx=10, pady=(10, 0))
    frame_arquivo = tk.Frame(root)
    frame_arquivo.pack(fill="x", padx=10)

    entrada_arquivo = tk.Entry(frame_arquivo)
    entrada_arquivo.pack(side="left", fill="x", expand=True)

    tk.Button(
        frame_arquivo,
        text="Procurar",
        command=lambda: selecionar_arquivo(entrada_arquivo),
    ).pack(side="left", padx=5)

    # Diretório de saída
    tk.Label(root, text="Diretório de salvamento:").pack(anchor="w", padx=10, pady=(10, 0))
    frame_diretorio = tk.Frame(root)
    frame_diretorio.pack(fill="x", padx=10)

    entrada_diretorio = tk.Entry(frame_diretorio)
    entrada_diretorio.pack(side="left", fill="x", expand=True)

    tk.Button(
        frame_diretorio,
        text="Procurar",
        command=lambda: selecionar_diretorio(entrada_diretorio)
    ).pack(side="left", padx=5)

    # Botão executar
    tk.Button(
        root,
        text="Executar",
        command=lambda: executar(entrada_arquivo, entrada_diretorio)
    ).pack(pady=15)

    root.mainloop()