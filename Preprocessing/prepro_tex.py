import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
def preprocessing_tex(df:pd.DataFrame,cols='About') -> pd.DataFrame:
    st=set(stopwords.words('english'))
    stemm=PorterStemmer()
    df[cols]=df[cols].apply(lambda x: " ".join([stemm.stem(i) for i in x.split() if i not in st]))
    return df