# src/validate.py
import pandas as pd
import json
import sys
import mlflow
from mlflow.tracking import MlflowClient
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def evaluate_lifecycle():
    # 1. Statistical Data Drift Profiling
    reference = pd.read_csv("data/baseline_training.csv")
    current = pd.read_csv("data/production_inference_logs.csv")
    
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference, current_data=current)
    report_dict = drift_report.as_dict()
    
    dataset_drift = report_dict["metrics"]["result"]["dataset_drift"]
    
    if dataset_drift:
        print("🚨 Data drift detected. Alerting team and terminating deployment pipeline.")
        sys.exit(1) # Block automated promotion step completely
        
    # 2. Model Registry Alias Promotion
    mlflow.set_tracking_uri("http://mlflow.internal:5000")
    client = MlflowClient()
    
    # Fetch latest registered model variant and tag as active deployment asset
    versions = client.get_latest_versions("user-churn-model", stages=["None"])
    latest_version = versions[0].version
    
    client.set_registered_model_alias("user-churn-model", "Production", latest_version)
    print(f"✅ Version {latest_version} promoted to active Production state inside registry.")

if __name__ == "__main__":
    evaluate_lifecycle()
