import pandas as pd
import re as r
def making_premiered(df:pd.DataFrame,col='Premiered') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())
    return df
def premeier_unk(df:pd.DataFrame,col='Premiered')-> pd.DataFrame :
    df[col]=df[col].apply(lambda x : 'Spring' if x=="Unknown" else x)
    return df 