# kubeflow/pipeline.py
from kfp import dsl
from kfp import compiler

@dsl.component(base_image="python:3.10-slim", packages_to_install=["pandas", "scikit-learn", "mlflow", "feast"])
def orchestrate_distributed_training(mlflow_uri: str, bucket_name: str):
    import pandas as pd
    import mlflow
    import sklearn.linear_model as lm
    from feast import FeatureStore
    from datetime import datetime
    
    # Extract Point-in-Time features from Feast
    store = FeatureStore(repo_path="feature_store")
    entity_df = pd.DataFrame({
        "user_id": [1001, 1002, 1003],
        "event_timestamp": [datetime.now(), datetime.now(), datetime.now()],
        "target": [0, 1, 0]
    })
    
    training_data = store.get_historical_features(
        entity_df=entity_df,
        features=["user_features:feature1", "user_features:feature2"]
    ).to_df()
    
    X = training_data[["feature1", "feature2"]]
    y = training_data["target"]
    
    model = lm.LogisticRegression()
    model.fit(X, y)
    
    # Log directly to Model Registry
    mlflow.set_tracking_uri(mlflow_uri)
    with mlflow.start_run():
        mlflow.log_param("algorithm", "LogisticRegression")
        mlflow.sklearn.log_model(model, "model", registered_model_name="user-churn-model")

@dsl.pipeline(name="e2e-churn-pipeline")
def e2e_pipeline(mlflow_uri: str, bucket_name: str):
    orchestrate_distributed_training(mlflow_uri=mlflow_uri, bucket_name=bucket_name)

if __name__ == "__main__":
    compiler.Compiler().compile(pipeline_func=e2e_pipeline, package_path="pipeline.yaml")
