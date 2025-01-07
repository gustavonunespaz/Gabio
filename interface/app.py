import tkinter as tk
from tkinter import filedialog

def run_app():
    window = tk.Tk()
    window.title("Gabio")

    tk.Button(window, text="Carregar MTR", command=carregar_mtr).pack(pady=10)
    tk.Button(window, text="Converter MTRs", command=converter_mtrs).pack(pady=10)

    window.mainloop()

def carregar_mtr():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    print(f"Arquivo Carregado: {file_path}")

def converter_mtrs():
    print("Conversão iniciada...")