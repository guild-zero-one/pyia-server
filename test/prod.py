import os
import pdfplumber

pdf_folder = "pdf"

# Lista todos os arquivos PDF da pasta
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Palavras-chave que identificam a tabela de produtos
keywords = ["produto", "descrição", "item", "quantidade", "preço", "valor"]

# Percorre cada PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"\n--- Lendo arquivo: {pdf_file} ---\n")
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table and table[0]:  # Garante que a tabela tem cabeçalho
                        header = [str(col).lower() for col in table[0]]
                        if any(
                            keyword in col for col in header for keyword in keywords
                        ):
                            print(f"\n--- Tabela encontrada na página {page_num} ---\n")
                            for row in table:
                                print(row)
