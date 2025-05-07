import pandas as pd
import sys
import os
import logging 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' )))
from Data_Reading.reading_csv import read_file
from Preprocessing.clean_nam import cleaning_Name
from Preprocessing.cleaning_tit import cleaning_Title
from Preprocessing.Demo import demo
from Preprocessing.genr import gen
from Preprocessing.making_prem import premeier_unk,making_premiered
from Preprocessing.merging_col import merg
from Preprocessing.prepro_tex import preprocessing_tex
from Preprocessing.prod import prodc
from Preprocessing.rat import rati
from Preprocessing.removeing_nan import remove_na
from Preprocessing.removing_unwant import rem
from Preprocessing.scr import sco
from Preprocessing.synops import syno
from Preprocessing.select_feature import sele_feature
from Preprocessing.sorc import sorc
from Preprocessing.studio_pr import studio_pre
from Preprocessing.themes import them

cols=["Title","Synopsis","Type","Premiered","Producers","Studios","Source","Genres","Themes","Demographics","Rating","Score"]
colu=["Title","English","Type","Premiered","Producers","Studios","Synopsis","Source","Genres","Themes","Demographics","Rating","Score"]
source_data=os.path.join("Data_Versioning","raw_data","Sample_df.csv")
preprocess_data=os.path.join("Data_Versioning","preprocessed","Preprocessed_anime.csv")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def preprocessing_pipeline():
    try:
        logging.info("**Step 1**: Doing the Data Reading for further work.")
        df=read_file(source_data)
        print("Shape of the data", df.shape)
        if df is None or df.empty:
            raise ValueError("The DataFrame is an Empty DataFrame")
        logging.info("**Step 2**: Preprocessing work for the Data starts from Here..")
        logging.info("....Selecting faeture for the basic Remommendation Model building....")
        df=sele_feature(df,colu)
        df=them(df,col='Themes')
        df=studio_pre(df,col='Studios')
        df=sorc(df,col="Source")
        df=syno(df,col='Synopsis')
        df=sco(df,col='Score')
        df=cleaning_Name(df,col='English')
        df=cleaning_Title(df,col='Title')
        df=demo(df,col='Demographics')
        df=gen(df,col='Genres')
        df=premeier_unk(df,col='Premiered')
        df=making_premiered(df,col='Premiered')
        df=prodc(df,col="Producers")
        df=rati(df,col='Rating')
        df=merg(df,col=cols)
        df=preprocessing_tex(df,cols='About')
        df=rem(df,cols)
        df.to_csv(preprocess_data)
        print("The columns in the datafrane",df.columns)
        logging.info(f"The Data has been cleaned and saved to a loctaion {preprocess_data}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except KeyError as e:
        logging.error(f"Missing column in dataset: {e}")
    except ValueError as e:
        logging.error(f"Value Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
if __name__=="__main__":
    preprocessing_pipeline()
             
