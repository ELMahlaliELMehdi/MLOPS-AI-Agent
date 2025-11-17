import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.mlflow_config import mlflow_config
import mlflow
from datetime import datetime
import yaml
from pathlib import Path

class ExperimentTracker:
    """
    Track agent experiments with MLflow
    """
    def __init__(self):
        self.current_run = None
        self.run_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "tool_usage": {}
        }
    
    def start_experiment(self, run_name: str = None):
        """
        Start a new experiment run
        """
        if not run_name:
            run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_run = mlflow_config.start_run(run_name=run_name)
        
        # Log agent configuration
        config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Log parameters
        mlflow.log_param("agent_name", config['agent']['name'])
        mlflow.log_param("agent_version", config['agent']['version'])
        mlflow.log_param("tools", ",".join(config['agent']['tools']))
        mlflow.log_param("reasoning_strategy", config['agent']['reasoning_strategy'])
        mlflow.log_param("max_history", config['agent']['max_history'])
        
        # Log artifact (config file)
        mlflow.log_artifact(str(config_path))
        
        return self.current_run
    
    def log_request(self, tool_name: str, success: bool, latency: float):
        """
        Log a single request
        """
        self.run_metrics["total_requests"] += 1
        
        if success:
            self.run_metrics["successful_requests"] += 1
        else:
            self.run_metrics["failed_requests"] += 1
        
        # Track tool usage
        if tool_name not in self.run_metrics["tool_usage"]:
            self.run_metrics["tool_usage"][tool_name] = 0
        self.run_metrics["tool_usage"][tool_name] += 1
        
        # Log metrics to MLflow
        if self.current_run:
            step = self.run_metrics["total_requests"]
            mlflow.log_metric("request_latency", latency, step=step)
            mlflow.log_metric("total_requests", self.run_metrics["total_requests"], step=step)
            mlflow.log_metric("success_rate", 
                            self.run_metrics["successful_requests"] / self.run_metrics["total_requests"] * 100,
                            step=step)
    
    def log_summary(self):
        """
        Log summary metrics at the end of run
        """
        if self.current_run:
            # Calculate averages
            total = self.run_metrics["total_requests"]
            if total > 0:
                success_rate = (self.run_metrics["successful_requests"] / total) * 100
                
                mlflow.log_metric("final_total_requests", total)
                mlflow.log_metric("final_success_rate", success_rate)
                mlflow.log_metric("final_failed_requests", self.run_metrics["failed_requests"])
                
                # Log tool usage
                for tool, count in self.run_metrics["tool_usage"].items():
                    mlflow.log_metric(f"tool_usage_{tool}", count)
    
    def end_experiment(self):
        """
        End the current experiment run
        """
        self.log_summary()
        mlflow_config.end_run()
        self.current_run = None

# Global experiment tracker
experiment_tracker = ExperimentTracker()