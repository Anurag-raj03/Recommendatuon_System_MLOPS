import pandas as pd
import re as r
def sorc(df:pd.DataFrame,col="Source") -> pd.DataFrame:
    df[col]=df[col].astype(str).apply(lambda x: r.sub("[^A-Za-z ]","",x).lower())
    return df