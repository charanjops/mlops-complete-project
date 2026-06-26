# src/generate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_dataset(num_users=1000, drift=False):
    np.random.seed(42 if not drift else 99)
    user_ids = np.arange(1001, 1001 + num_users)
    
    # Simulate features
    mu = 50 if not drift else 35 # Shift mean downward to simulate feature drift
    feature1 = np.random.normal(loc=mu, scale=10, size=num_users)
    feature2 = np.random.normal(loc=15, scale=3, size=num_users)
    
    # Ground truth rules
    target = (feature1 * 0.4 - feature2 * 0.8 + np.random.normal(0, 2, num_users)) > 5
    target = target.astype(int)
    
    timestamps = [datetime.now() - timedelta(days=np.random.randint(1, 30)) for _ in range(num_users)]
    
    df = pd.DataFrame({
        "user_id": user_ids,
        "event_timestamp": timestamps,
        "feature1": feature1,
        "feature2": feature2,
        "target": target
    })
    return df

if __name__ == "__main__":
    # Generate baseline data tracking
    df_base = create_dataset(1000, drift=False)
    df_base.to_parquet("data/features.parquet")
    df_base.to_csv("data/baseline_training.csv", index=False)
    
    # Generate drifted inference data log profile
    df_drift = create_dataset(500, drift=True)
    df_drift.to_csv("data/production_inference_logs.csv", index=False)
    print("✅ Synthetic datasets created successfully.")
