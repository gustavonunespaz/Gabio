import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# Variável global para armazenar o caminho do arquivo selecionado
selected_file = None

def run_app():
    window = tk.Tk()
    window.title("Gabio")

    tk.Button(window, text="Carregar MTR", command=carregar_mtr).pack(pady=10)
    tk.Button(window, text="Converter MTRs", command=converter_mtrs).pack(pady=10)

    window.mainloop()

def carregar_mtr():
    global selected_file
    file_paths = filedialog.askopenfilename(
        filetypes=[("Arquivos PDF", "*.pdf")],
        title="Selecione um ou mais arquivos MTR"
    )
    if file_paths:
        selected_file = list(file_paths)
        messagebox.showinfo("Arquivos selecionados", f"{len(file_paths)} Arquivo selecionado: {file_paths}")
    else:
        messagebox.showinfo("Nenhum arquivo", "Nenhum arquivo foi selecionado.")

def converter_mtrs():
    global selected_file
    if not selected_file:
        messagebox.showinfo("Aviso", "Nenhum arquivo foi selecionado. Carregue um arquivo primeiro.")
        return  # Encerra a função caso nenhum arquivo tenha sido carregado

    try:
        with open(selected_file, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()

        print("Conteúdo Extraído:")
        print(content)

        messagebox.showinfo("Sucesso", "Arquivo convertido com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao converter o arquivo: {str(e)}")

# Iniciar o aplicativo
if __name__ == "__main__":
    run_app()
