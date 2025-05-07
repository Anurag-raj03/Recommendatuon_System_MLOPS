import pandas as pd
import re as r
def cleaning_Title(df:pd.DataFrame,col='Title') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())  
    return df 