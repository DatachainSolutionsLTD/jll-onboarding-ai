import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

import xgboost as xgb

# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

BASE_DIR = "/Users/sangeetha/Desktop/jll-onboarding-ai"

DATASET_PATH = BASE_DIR + "/data/processed/fm_training_dataset.csv"
MODEL_PATH = BASE_DIR + "/models"

os.makedirs(MODEL_PATH, exist_ok=True)

# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------

print("Loading training dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)

print(df.head())

# -------------------------------------------------
# DEFINE FEATURES AND LABEL
# -------------------------------------------------

features = [
    "role_title",
    "is_manager",
    "function",
    "region",
    "country",
    "device_platform",
    "ram",
    "installed_app_count"
]

label = "bundle_tier"

X = df[features].copy()
y = df[label]

# -------------------------------------------------
# ENCODE CATEGORICAL FEATURES
# -------------------------------------------------

print("Encoding categorical features...")

encoders = {}

for col in X.columns:
    if X[col].dtype == "object":

        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col].astype(str))

        encoders[col] = encoder

# encode target label
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -------------------------------------------------
# TRAIN TEST SPLIT
# -------------------------------------------------

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)

# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

print("Training XGBoost model...")


model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    objective="multi:softprob",
    subsample=0.8,
    colsample_bytree=0.8
)
model.fit(X_train, y_train)

# -------------------------------------------------
# MODEL EVALUATION
# -------------------------------------------------

print("Evaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# -------------------------------------------------
# SAVE MODEL
# -------------------------------------------------

model_file = MODEL_PATH + "/fm_bundle_classifier_xgboost.pkl"
encoder_file = MODEL_PATH + "/feature_encoders.pkl"
label_file = MODEL_PATH + "/label_encoder.pkl"

joblib.dump(model, model_file)
joblib.dump(encoders, encoder_file)
joblib.dump(label_encoder, label_file)

print("\nModel saved successfully!")

print("Model file:", model_file)
print("Encoders:", encoder_file)
print("Label encoder:", label_file)
