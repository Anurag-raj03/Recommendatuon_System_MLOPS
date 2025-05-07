import pandas as pd
import re as r
def cleaning_Name(df:pd.DataFrame,col='English') -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z0-9 ]","",x).lower())  
    return df 