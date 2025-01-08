from pytesseract import pytesseract
from PIL import Image
from spellchecker import SpellChecker
from textblob import TextBlob
import re

# Configuração do Tesseract
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Inicializar o corretor ortográfico
spell = SpellChecker(language="pt")

# Função para corrigir texto com SpellChecker
def corrigir_texto(texto):
    palavras_corrigidas = TextBlob(texto).correct()
    return str(palavras_corrigidas)

# Função para selecionar a imagem
from tkinter import filedialog

def selecionar_imagem():
    print("[INFO] Escolha a imagem na janela que será aberta...")
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        print("[ERRO] Nenhuma imagem selecionada.")
        return None
    print(f"[INFO] Imagem selecionada: {file_path}\n")
    return file_path

# Função para extrair texto da imagem
def extrair_texto_da_imagem(image_path):
    try:
        img = Image.open(image_path)
        texto_bruto = pytesseract.image_to_string(img, lang="por")
        print("\n=== Texto Extraído Bruto ===")
        print(texto_bruto)
        return texto_bruto
    except Exception as e:
        print(f"[ERRO] Falha ao processar a imagem: {e}")
        return None

# Função para extrair dados do texto
def extrair_dados(texto):
    if not texto:
        print("[ERRO] Nenhum texto para processar.")
        return {}

    dados = {
        "Número MTR": re.search(r"MTR nº: (\d+)", texto),
        "Código IBAMA": re.search(r"Código IBAMA.*?(\d+)", texto),
        "Denominação": re.search(r"Denominação.*?:(.*?)(?:\n|Estado Físico)", texto, re.DOTALL),
        "Estado Físico": re.search(r"Estado Físico\s*:\s*(\w+)", texto),
        "Classe": re.search(r"Classe\s*:\s*(\w+)", texto),
        "Acondicionamento": re.search(r"Acondicionamento\s*:\s*(\w+)", texto),
        "Qtde": re.search(r"Qtde\s*:\s*(\d+,\d+)", texto),
        "Unidade": re.search(r"Unidade\s*:\s*(\w+)", texto),
        "Tratamento": re.search(r"Tratamento\s*:\s*(.*)", texto),
        "Identificação do Gerador": re.search(r"Identificação do Gerador.*?Razão Social: (.*?)CPF", texto, re.DOTALL),
        "Identificação do Transportador": re.search(r"Identificação do Transportador.*?Razão Social: (.*?)CPF", texto, re.DOTALL),
        "Identificação do Destinador": re.search(r"Identificação do Destinador.*?Razão Social: (.*?)CPF", texto, re.DOTALL),
        "Data do Transporte": re.search(r"Data do transporte:\s*(\d{2}/\d{2}/\d{4})", texto),
        "Data do Recebimento": re.search(r"Data do recebimento:\s*(\d{2}/\d{2}/\d{4})", texto),
    }

    # Corrigir valores para evitar NoneType
    for chave, valor in dados.items():
        dados[chave] = valor.group(1).strip() if valor else "Não informado"

    return dados

# Função principal
def main():
    image_path = selecionar_imagem()
    if not image_path:
        return

    texto_extraido = extrair_texto_da_imagem(image_path)
    if not texto_extraido:
        return

    texto_corrigido = corrigir_texto(texto_extraido)
    dados_extraidos = extrair_dados(texto_corrigido)

    print("\n--- Dados Gerais ---")
    for chave, valor in dados_extraidos.items():
        print(f"{chave}: {valor}")

if __name__ == "__main__":
    main()
