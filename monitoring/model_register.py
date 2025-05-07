import mlflow
import mlflow.tracking
def register_model():
    mlflow.set_tracking_uri("http://mlflow:5000")
    experi_name="MLOPS_RECOMMENDATION_SYSTEM"
    if not mlflow.get_experiment_by_name(experi_name):
        experi_id=mlflow.create_experiment(experi_name)
        print(f"Experiment with {experi_name} and with {experi_id} Created Successfully")
    else:
        experi_id=mlflow.get_experiment_by_name(experi_name).experiment_id
        print(f"Your Existing experiment {experi_name} with ID: {experi_id}")
        mlflow.set_experiment(experi_name) 
        client=mlflow.tracking.MlflowClient()
        runs=client.search_runs(experi_id,order_by=["start_time DESC"],max_results=1)
        
        if not runs:
            print("No recent runs found with a logged Artifacts.")
            return
        current_run_id=runs[0].info.run_id
        print(f"latest run ID: {current_run_id}")
        
        artifacts=client.list_artifacts(current_run_id) 
        artifact_path=[i.path for i in artifacts] 
        
        if not artifact_path:
            print(f"Experiment is Created Freshly, Hence No Artifacts will be found in this run")
            return
        print("Artifact Found")
        for i in artifact_path:
            print(f"  -{i}")

if __name__ == "__main__":
    register_model()
         
        
        
            
              
            
            
            
            
            
        