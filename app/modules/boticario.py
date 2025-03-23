import pandas as pd

from app.gemini import gen
from app.utils.pdf_transform import transform_df


def create_df(content: str):
    # Apagando texto desnecessário
    remove_data = content.split("\nIPI\nICMS")
    remove_data = remove_data[1].split("RESERVADO AO FISCO")

    lines = remove_data[0].strip().split("\n")

    # Colunas do DataFrame
    header = [
        "CÓD. PRODUTO",
        "DESCRIÇÃO DOS PRODUTOS/SERVIÇOS",
        "NCM/SH",
        "CST",
        "CFOP",
        "UNID.",
        "QUANT.",
        "VALOR UNITÁRIO",
        "VALOR TOTAL",
        "B.CALC.ICMS",
        "VALOR ICMS",
        "VALOR I.P.I.",
        "A. IPI",
        "A. ICMS",
    ]

    data = []
    for i in range(0, len(lines), 14):
        row = lines[i : i + 14]
        data.append(row)

    df = pd.DataFrame(data, columns=header)
    transform_df(df)

    return gen.gen_json()
