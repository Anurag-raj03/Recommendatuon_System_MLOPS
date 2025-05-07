from airflow.decorators import task
print("Transform task started...")
@task
def transform_data():
    import pandas as pd
    import os
    import sys

    print("Transform task started...")
    conn = None
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Database_connection.db_init import get_connection, insert_preprocessed_data
    from Data_Reading.reading_csv import read_file
    from Preprocessing.clean_nam import cleaning_Name
    from Preprocessing.cleaning_tit import cleaning_Title
    from Preprocessing.Demo import demo
    from Preprocessing.genr import gen
    from Preprocessing.making_prem import premeier_unk, making_premiered
    from Preprocessing.merging_col import merg
    from Preprocessing.prepro_tex import preprocessing_tex
    from Preprocessing.prod import prodc
    from Preprocessing.rat import rati
    from Preprocessing.removing_unwant import rem
    from Preprocessing.scr import sco
    from Preprocessing.synops import syno
    from Preprocessing.select_feature import sele_feature
    from Preprocessing.sorc import sorc
    from Preprocessing.studio_pr import studio_pre
    from Preprocessing.themes import them
    try:
  
        db_path = "/opt/airflow/Database_connection/anime_preprocessed_dat.db"
        etl_path = os.path.join("Data_Versioning", "ETL_Data", "extracted_data.csv")

        conn = get_connection(db_path)
        if conn is None:
            print("Failed to establish database connection.")
            return
        cols = ["Title", "Synopsis", "Type", "Premiered", "Producers", "Studios", "Source", "Genres", "Themes", "Demographics", "Rating", "Score"]
        colu = ["Title", "English", "Type", "Premiered", "Producers", "Studios", "Synopsis", "Source", "Genres", "Themes", "Demographics", "Rating", "Score"]

        print("Reading extracted CSV...")
        df = read_file(etl_path)
        if df is None or df.empty:
            raise ValueError("The Reading DataFrame is Empty or Not Found.")

        print("Preprocessing started...")
        df = sele_feature(df, colu)
        df = them(df, col='Themes')
        df = studio_pre(df, col='Studios')
        df = sorc(df, col="Source")
        df = syno(df, col='Synopsis')
        df = sco(df, col='Score')
        df = cleaning_Name(df, col='English')
        df = cleaning_Title(df, col='Title')
        df = demo(df, col='Demographics')
        df = gen(df, col='Genres')
        df = premeier_unk(df, col='Premiered')
        df = making_premiered(df, col='Premiered')
        df = prodc(df, col="Producers")
        df = rati(df, col='Rating')
        df = merg(df, col=cols)
        df = preprocessing_tex(df, cols='About')
        df = rem(df, cols)

        if df.empty:
            print("No data to insert into database.")
            return
        print("Inserting preprocessed data into database...")
        insert_preprocessed_data(conn, df)

        print(f"Preprocessing complete. Final shape: {df.shape}")

    except Exception as e:
        print(f"Error in transform_data task: {e}")
