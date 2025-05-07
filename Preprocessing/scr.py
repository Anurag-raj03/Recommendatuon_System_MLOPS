import pandas as pd 
import re as r
def sco(df:pd.DataFrame,col='Score') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^0-9. ]","",x).lower())
    return df