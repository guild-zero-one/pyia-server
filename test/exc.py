import os
import pandas as pd
import pdfplumber

# Caminho da pasta onde sempre terá um único arquivo PDF
pdf_folder = "pdf"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

if pdf_files:  # Verifica se há um arquivo na pasta
    pdf_path = os.path.join(pdf_folder, pdf_files[0])  # Pega o único PDF
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page_num, page in enumerate(pdf.pages, start=1):
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                df["Página"] = page_num  # Adiciona a página de origem
                all_tables.append(df)

        if all_tables:
            final_df = pd.concat(all_tables, ignore_index=True)
            # Salva em TXT, formatado de forma legível
            with open("./upload/produtos.txt", "w") as f:
                f.write(final_df.to_string(index=False))
            print("Arquivo TXT criado com sucesso!")
        else:
            print("Nenhuma tabela encontrada no arquivo PDF.")
else:
    print("Nenhum arquivo PDF encontrado na pasta.")
