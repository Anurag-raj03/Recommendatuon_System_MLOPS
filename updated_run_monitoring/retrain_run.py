

def rerun_pipeline(preprocess_data_path:str, cosine_sim_path:str) -> None:
    import os 
    import pandas as pd
    import sys
    import logging
    import mlflow
    import joblib as j
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Data_Reading.reading_csv import read_file

    tf_vectorizer_path = os.path.join("artifacts", "anime_vectorizer.jbl")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    try:
        mlflow.set_tracking_uri("http://mlflow:5000")
        mlflow.set_experiment("MLOPS_RECOMMENDATION_SYSTEM")

        logging.info("**Step 3: Making a TFIDF Vectorizer for the corpus of the Words we have for the Recommendation System...")
        tf_vectorizer = TfidfVectorizer()

        logging.info("Reintializing the Preprocessed Data for the work")
        df = read_file(preprocess_data_path)

        logging.info("....Making the Text into the Vectors for making the closest Recommendation...")
        vectors = tf_vectorizer.fit_transform(df['About']).toarray()

        logging.info("**Step 4: Now making the Cosine Similarity method to find the Recommended ones...")
        similarity_vec = cosine_similarity(vectors)
        
        logging.info(".....Saving Every artifact file in the directory for the as Joblib file for futher use....")
        j.dump(tf_vectorizer, tf_vectorizer_path)
        j.dump(similarity_vec, cosine_sim_path)

        logging.info("**Step 6: Logging All Artifacts no model making is Involved in this, Input Example to MLflow**")
        with mlflow.start_run():
            mlflow.log_artifact(tf_vectorizer_path)
            mlflow.log_artifact(cosine_sim_path)
            mlflow.log_metrics({"num_rows": len(df), "num_columns": df.shape[1]})
            mlflow.log_param("Model_type", "Cosine Similarity + TF-IDF Vectorizer")

        logging.info("**All Artifacts File Has been Saved Successfully in MLFLOW artifacts**")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except KeyError as e:
        logging.error(f"Missing column in dataset: {e}")
    except ValueError as e:
        logging.error(f"Value Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

"""Without MLFLOW for faster execution"""
# def rerun_pipeline(preprocess_data_path: str, cosine_sim_path: str) -> None:
#     import os 
#     import pandas as pd
#     import sys
#     import logging
#     import mlflow
#     import joblib as j
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.metrics.pairwise import cosine_similarity

#     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     from Data_Reading.reading_csv import read_file

#     tf_vectorizer_path = os.path.join("artifacts", "anime_vectorizer.jbl")

#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
#     logging.info("**Step 3: Making a TFIDF Vectorizer for the corpus of the Words we have for the Recommendation System...**")
#     tf_vectorizer = TfidfVectorizer()

#     logging.info("Reinitializing the Preprocessed Data for the work...")
#     df = read_file(preprocess_data_path)

#     logging.info("....Making the Text into the Vectors for making the closest Recommendation...")
#     vectors = tf_vectorizer.fit_transform(df['About']).toarray()

#     logging.info("**Step 4: Now making the Cosine Similarity method to find the Recommended ones...")
#     similarity_vec = cosine_similarity(vectors)

#     logging.info(".....Saving Every artifact file in the directory as Joblib files for further use....")
#     j.dump(tf_vectorizer, tf_vectorizer_path)
#     j.dump(similarity_vec, cosine_sim_path)

#     logging.info("✅ Artifacts File Saved Successfully.")