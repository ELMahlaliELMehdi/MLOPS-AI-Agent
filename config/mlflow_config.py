import mlflow
import os
from pathlib import Path

class MLflowConfig:
    """
    MLflow configuration and setup
    """
    def __init__(self, experiment_name: str = "ai-agent-experiments"):
        self.experiment_name = experiment_name
        
        # Use environment variable for tracking URI (Docker-friendly)
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
        
        # Set tracking URI
        mlflow.set_tracking_uri(self.tracking_uri)
        
        # Set or create experiment
        try:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        except:
            # Experiment already exists
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment:
                self.experiment_id = experiment.experiment_id
        
        mlflow.set_experiment(experiment_name)
    
    def log_agent_config(self, config: dict):
        """
        Log agent configuration parameters
        """
        with mlflow.start_run(run_name="agent_config"):
            # Log parameters
            for key, value in config.items():
                mlflow.log_param(key, value)
    
    def log_run_metrics(self, metrics: dict, step: int = None):
        """
        Log metrics for a run
        """
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
    
    def log_artifact(self, file_path: str):
        """
        Log an artifact (file)
        """
        mlflow.log_artifact(file_path)
    
    def start_run(self, run_name: str = None):
        """
        Start a new MLflow run
        """
        return mlflow.start_run(run_name=run_name)
    
    def end_run(self):
        """
        End the current MLflow run
        """
        mlflow.end_run()

# Global MLflow config instance
mlflow_config = MLflowConfig()