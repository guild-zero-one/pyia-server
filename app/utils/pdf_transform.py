"""PDF Transformation"""

import pandas as pd


def transform_df(df: pd.DataFrame):
    df.to_string(buf="app/upload/products.txt", index=False)
