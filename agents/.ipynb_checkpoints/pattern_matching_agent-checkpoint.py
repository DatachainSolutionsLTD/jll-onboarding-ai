import joblib
import pandas as pd
import os

# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_FILE = os.path.join(MODEL_DIR, "fm_bundle_classifier_xgboost.pkl")
ENCODER_FILE = os.path.join(MODEL_DIR, "feature_encoders.pkl")
LABEL_FILE = os.path.join(MODEL_DIR, "label_encoder.pkl")

print("Loading model from:", MODEL_FILE)

# -------------------------------------------------
# LOAD MODEL + ENCODERS
# -------------------------------------------------

model = joblib.load(MODEL_FILE)
encoders = joblib.load(ENCODER_FILE)
label_encoder = joblib.load(LABEL_FILE)

print("Model loaded successfully")

# -------------------------------------------------
# TRAINING FEATURE ORDER (IMPORTANT)
# -------------------------------------------------

FEATURE_COLUMNS = [
    "role_title",
    "is_manager",
    "function",
    "region",
    "country",
    "device_platform",
    "ram",
    "installed_app_count"
]

# -------------------------------------------------
# PREDICTION FUNCTION
# -------------------------------------------------

def predict_bundle(user_profile):

    filtered_data = {k: user_profile.get(k) for k in FEATURE_COLUMNS}

    df = pd.DataFrame([filtered_data])

    # encode categorical features
    for col, encoder in encoders.items():

        if col in df.columns:

            value = df[col].astype(str)

            known_classes = set(encoder.classes_)

            df[col] = [
                encoder.transform([v])[0] if v in known_classes else -1
                for v in value
            ]

    # ensure correct feature order
    df = df[FEATURE_COLUMNS]

    # predict bundle
    prediction = model.predict(df)

    predicted_label = label_encoder.inverse_transform(prediction)

    return predicted_label[0]


# -------------------------------------------------
# TEST AGENT
# -------------------------------------------------

if __name__ == "__main__":

    sample_user = {
        "role_title": "Facilities Manager",
        "is_manager": "Yes",
        "function": "Facilities",
        "region": "EMEA",
        "country": "UK",
        "device_platform": "Windows",
        "ram": 16,
        "installed_app_count": 25
    }

    bundle = predict_bundle(sample_user)

    print("\nPredicted Bundle Tier:", bundle)