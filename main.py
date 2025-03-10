import os

import pandas as pd
import pdfplumber

# Caminho da pasta onde estão os PDFs
pdf_folder = "pdf"

# Lista todos os arquivos da pasta
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Percorre cada PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                print(f"Conteúdo do arquivo: {pdf_file}")
                print(df)


# for pdf_file in pdf_files:
#     pdf_path = os.path.join(pdf_folder, pdf_file)
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             # text = page.extract_text()
#             # print(text)

#             table = page.extract_tables()
#             print(table)
