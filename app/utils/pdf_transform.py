"""PDF Transformation"""

import pandas as pd


def transform_df(df: pd.DataFrame):
    df.to_string(buf="app/upload/p.txt", index=False)
    return df
