import pandas as pd
import re as r
def rati(df:pd.DataFrame,col='Rating') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())
    return df