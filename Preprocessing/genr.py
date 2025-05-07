import pandas as pd
import re as r
def gen(df:pd.DataFrame,col='Genres') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())
    return df