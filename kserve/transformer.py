# kserve/transformer.py
import kserve
from typing import Dict
from feast import FeatureStore
import os

class FeastDataTransformer(kserve.Model):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.store = None

    def load(self):
        # Establish link to Feast Redis Online Cluster
        self.store = FeatureStore(repo_path="/mnt/models/feature_store")

    def preprocess(self, payload: Dict, headers: Dict = None) -> Dict:
        user_id = payload["user_id"]
        
        feature_vector = self.store.get_online_features(
            features=["user_features:feature1", "user_features:feature2"],
            entity_rows=[{"user_id": user_id}]
        ).to_dict()
        
        return {"instances": [[feature_vector["feature1"], feature_vector["feature2"]]]}

    def postprocess(self, response: Dict, headers: Dict = None) -> Dict:
        return response

if __name__ == "__main__":
    transformer = FeastDataTransformer("user-churn-transformer", predictor_host=os.getenv("PREDICTOR_HOST"))
    kserve.ModelServer().start([transformer])
