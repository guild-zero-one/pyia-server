import pandas as pd


def text_to_dataframe(text):
    lines = text.strip().split("\n")

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
    df.to_string(buf="app/upload/p.txt", index=False)

    return df
