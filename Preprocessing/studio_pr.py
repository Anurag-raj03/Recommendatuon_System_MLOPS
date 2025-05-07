import pandas as pd
import re as r
def studio_pre(df:pd.DataFrame,col='Studios') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: x.split(',')[0].lower())
    return df 