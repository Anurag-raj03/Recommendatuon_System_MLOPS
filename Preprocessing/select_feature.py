import pandas as pd
colu=["Title","English","Type","Premiered","Producers","Studios","Synopsis","Source","Genres","Themes","Demographics","Rating","Score"]
def sele_feature(df:pd.DataFrame,col=colu) -> pd.DataFrame:
    for i in df.columns:
       if i not in col:
           df.drop(i,axis=1,inplace=True)
    return df       