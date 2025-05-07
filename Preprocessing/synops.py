import re as r
import pandas as pd
def syno(df:pd.DataFrame,col='Synopsis') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())
    return df