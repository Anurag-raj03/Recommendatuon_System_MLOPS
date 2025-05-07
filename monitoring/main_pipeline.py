import os 
import pandas as pd
import sys
import logging
import mlflow
import joblib as j
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sklearn.feature_extraction.text import TfidfVectorizer
app = FastAPI()
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Data_Reading.reading_csv import read_file


mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("MLOPS_RECOMMENDATION_SYSTEM")
preprocess_data=os.path.join("Data_Versioning","preprocessed","Preprocessed_anime.csv")
mlflow_input_csv=os.path.join("DATA","mlflow_example_input.csv")
tf_vectorizer_path=os.path.join("artifacts","anime_vectorizer.jbl")
cosine_sim_path=os.path.join("artifacts","anime_cosine.jbl")
example_vectors_path=os.path.join("artifacts","example_vec.jbl")  
example_cosine_path=os.path.join("artifacts","example_cos.jbl")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    try:
        logging.info("**Step 3: Making a TFIDF Vectorizer for the corpus of the Words we have for the Recommendation System...")
        tf_vectorizer=TfidfVectorizer()
        logging.info("Reintailizing the Preprocessed Data for the work")
        df=read_file(preprocess_data)
        logging.info("....Making the Text into the Vectors for making the closest Recommendation...")
        vectors=tf_vectorizer.fit_transform(df['About']).toarray()
        logging.info("**Step 4: Now making the Cosine Simarity method to find the Recommended ones...")
        simalarity_vec=cosine_similarity(vectors)
        
        logging.info("**Step 5: Before Giving the Signature Example as mlflow_input_example.csv Working for Checking....")
        input_exam=read_file(mlflow_input_csv)
        signature_vec=tf_vectorizer.transform(input_exam['About']).toarray()
        logging.info("....Checking is Done. Moving for the Next part.....")
        signature_sim=cosine_similarity(signature_vec)
        logging.info(".....Saving Every artifact file in the directory for the as Joblib file for futher use....")
        j.dump(tf_vectorizer,tf_vectorizer_path)
        j.dump(simalarity_vec,cosine_sim_path)
        j.dump(signature_vec,example_vectors_path)
        j.dump(signature_sim,example_cosine_path)
        logging.info("**Step 6: Logging All Artifacts no model making is Involved in this,Input Example to MLflow**")
        with mlflow.start_run():
            mlflow.log_artifact(tf_vectorizer_path)
            mlflow.log_artifact(cosine_sim_path)
            mlflow.log_artifact(example_vectors_path)
            mlflow.log_artifact(example_cosine_path)
            mlflow.log_artifact(mlflow_input_csv)
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
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)           
        
if __name__=="__main__":
     run_pipeline()       
        
        
        
        
        
        
        






