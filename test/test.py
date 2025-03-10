import pdfplumber

pdf_folder = "pdf"

# Lista todos os arquivos PDF da pasta
import os

pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Percorre cada PDF e imprime todo o conteúdo
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"\n--- Conteúdo do arquivo: {pdf_file} ---\n")
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Imprime o texto da página
            text = page.extract_text()
            if text:
                print(f"\n--- Texto da página {page_num} ---\n")
                print(text)

            # Imprime as tabelas da página
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    print(f"\n--- Tabela da página {page_num} ---\n")
                    for row in table:
                        print(row)
