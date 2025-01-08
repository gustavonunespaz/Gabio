import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import openpyxl

# Variáveis globais
selected_files = []
excel_data = []
table = None

def run_app():
    global table

    # Janela principal
    window = tk.Tk()
    window.title("Gabio - Controle de MTRs")
    window.geometry("1600x800")
    window.configure(bg="#f0f0f0")

    # Centraliza a janela na tela
    window.eval('tk::PlaceWindow . center')

    # Frame de botões
    button_frame = tk.Frame(window, bg="#d9d9d9", relief=tk.RIDGE, bd=2)
    button_frame.pack(fill=tk.X, pady=5)

    tk.Button(button_frame, text="Carregar MTR", command=carregar_mtr, bg="#4CAF50", fg="white", width=20).pack(side=tk.LEFT, padx=10, pady=5)
    tk.Button(button_frame, text="Converter MTRs", command=converter_mtrs, bg="#2196F3", fg="white", width=20).pack(side=tk.LEFT, padx=10, pady=5)

    # Frame da tabela
    table_frame = tk.Frame(window, bg="#ffffff", relief=tk.SUNKEN, bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Barra de rolagem horizontal e vertical
    x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Configuração da tabela
    columns = [
        "Número MTR", "Código IBAMA", "Denominação", "Estado Físico", "Classe",
        "Acondicionamento", "Quantidade (toneladas)", "Quantidade (Kg)", "Tratamento",
        "Identificação do Gerador", "Identificação do Transportador", "Identificação do Destinador",
        "Data do Transporte", "Data do Recebimento"
    ]

    table = ttk.Treeview(
        table_frame, columns=columns, show="headings", height=20,
        xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set
    )
    # Definir larguras personalizadas
    column_widths = {
        "Número MTR": 100,
        "Código IBAMA": 100,
        "Denominação": 150,
        "Estado Físico": 120,
        "Classe": 100,
        "Acondicionamento": 150,
        "Quantidade (toneladas)": 150,
        "Quantidade (Kg)": 150,
        "Tratamento": 150,
        "Identificação do Gerador": 200,
        "Identificação do Transportador": 200,
        "Identificação do Destinador": 200,
        "Data do Transporte": 150,
        "Data do Recebimento": 150
    }

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=column_widths.get(col, 150), anchor="center")

    table.pack(fill=tk.BOTH, expand=True)
    x_scroll.config(command=table.xview)
    y_scroll.config(command=table.yview)

    window.mainloop()

def carregar_mtr():
    global selected_files, excel_data, table
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Arquivos PDF", "*.pdf")],
        title="Selecione um ou mais arquivos MTR"
    )
    if file_paths:
        selected_files = list(file_paths)
        messagebox.showinfo("Arquivos selecionados", f"{len(file_paths)} arquivo(s) carregado(s).")

        # Processar os PDFs e atualizar a tabela
        excel_data = []
        for file_path in selected_files:
            data = process_pdf(file_path)
            excel_data.append(data)
        
        atualizar_tabela()
    else:
        messagebox.showinfo("Nenhum arquivo", "Nenhum arquivo foi selecionado.")

def process_pdf(file_path):
    """
    Processa o PDF e extrai os dados.
    """
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()

        # Simula a extração de dados com base no conteúdo
        return {
            "Número MTR": extract_data(content, "Número MTR:", "Código IBAMA"),
            "Código IBAMA": extract_data(content, "Código IBAMA:", "Denominação"),
            "Denominação": extract_data(content, "Denominação:", "Estado Físico"),
            "Estado Físico": extract_data(content, "Estado Físico:", "Classe"),
            "Classe": extract_data(content, "Classe:", "Acondicionamento"),
            "Acondicionamento": extract_data(content, "Acondicionamento:", "Quantidade (toneladas)"),
            "Quantidade (toneladas)": extract_data(content, "Quantidade (toneladas):", "Quantidade (Kg)"),
            "Quantidade (Kg)": extract_data(content, "Quantidade (Kg):", "Tratamento"),
            "Tratamento": extract_data(content, "Tratamento:", "Identificação do Gerador"),
            "Identificação do Gerador": extract_data(content, "Identificação do Gerador:", "Identificação do Transportador"),
            "Identificação do Transportador": extract_data(content, "Identificação do Transportador:", "Identificação do Destinador"),
            "Identificação do Destinador": extract_data(content, "Identificação do Destinador:", "Data do Transporte"),
            "Data do Transporte": extract_data(content, "Data do Transporte:", "Data do Recebimento"),
            "Data do Recebimento": extract_data(content, "Data do Recebimento:", "\n")
        }
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo {file_path}: {e}")
        return {}

def extract_data(content, start, end):
    """
    Extrai dados específicos do texto com base em delimitadores.
    """
    try:
        start_idx = content.index(start) + len(start)
        end_idx = content.index(end, start_idx)
        return content[start_idx:end_idx].strip()
    except ValueError:
        return ""

def atualizar_tabela():
    """
    Atualiza a tabela com os dados extraídos.
    """
    global table, excel_data
    table.delete(*table.get_children())
    for data in excel_data:
        row = [data.get(col, "") for col in table["columns"]]
        table.insert("", tk.END, values=row)

def converter_mtrs():
    global excel_data
    if not excel_data:
        messagebox.showinfo("Aviso", "Nenhum dado disponível para exportar. Carregue os PDFs primeiro.")
        return

    try:
        # Cria uma nova planilha de Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Controle MTRs"

        # Adiciona os cabeçalhos
        headers = table["columns"]
        sheet.append(headers)

        # Adiciona os dados
        for data in excel_data:
            sheet.append([data.get(col, "") for col in headers])

        # Salva o arquivo Excel
        output_file = "Controle_MTRs.xlsx"
        workbook.save(output_file)

        messagebox.showinfo("Sucesso", f"Arquivo Excel salvo como '{output_file}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo Excel: {e}")

# Iniciar o aplicativo
if __name__ == "__main__":
    run_app()
