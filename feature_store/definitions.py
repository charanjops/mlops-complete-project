# feature_store/definitions.py
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float32

user_entity = Entity(name="user_id", value_type=ValueType.INT64)

offline_source = FileSource(
    path="s3://my-mlops-bucket/features/features.parquet",
    event_timestamp_column="event_timestamp",
)

user_features_view = FeatureView(
    name="user_features",
    entities=[user_entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="feature1", dtype=Float32),
        Field(name="feature2", dtype=Float32),
    ],
    online=True,
    source=offline_source,
)
