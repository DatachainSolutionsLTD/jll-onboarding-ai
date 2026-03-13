import pandas as pd
import os
import random

print("Starting dataset build...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUTPUT_PATH, exist_ok=True)

people_file = os.path.join(
    RAW_DATA_PATH,
    "Extract of November People and Persona file.xlsx"
)

print("Loading People & Persona file...")

people_df = pd.read_excel(people_file)

print("People file shape:", people_df.shape)

# ------------------------------------------------
# Select Facilities related users
# ------------------------------------------------

fm_users = people_df[
    people_df["Business Title"]
    .astype(str)
    .str.contains("Manager|Director|Operations", case=False, na=False)
].copy()

print("Filtered FM users:", fm_users.shape)

# ------------------------------------------------
# Feature simulation
# ------------------------------------------------

regions = ["EMEA", "AMER", "APAC"]
platforms = ["Windows", "Mac", "Linux"]
ram_options = [8, 16, 32, 64]

dataset_rows = []

for _, row in fm_users.iterrows():

    installed_apps = random.randint(10, 60)
    ram = random.choice(ram_options)
    region = random.choice(regions)
    device = random.choice(platforms)

    is_manager = "Yes" if "Manager" in str(row["Business Title"]) else "No"

    record = {
        "role_title": row["Business Title"],
        "is_manager": is_manager,
        "function": row.get("Function", "Facilities"),
        "region": region,
        "country": row.get("Country", "UK"),
        "device_platform": device,
        "ram": ram,
        "installed_app_count": installed_apps
    }

    dataset_rows.append(record)

dataset = pd.DataFrame(dataset_rows)

# ------------------------------------------------
# Bundle assignment logic
# ------------------------------------------------

def assign_bundle(row):

    apps = row["installed_app_count"]
    ram = row["ram"]
    manager = row["is_manager"]

    if apps < 20 and ram <= 16:
        return "FM_BASE"

    if apps < 30:
        return "BUNDLE_1"

    if apps < 45 or manager == "Yes":
        return "BUNDLE_2"

    return "BUNDLE_3"

dataset["bundle_tier"] = dataset.apply(assign_bundle, axis=1)

# ------------------------------------------------
# Save dataset
# ------------------------------------------------

output_file = os.path.join(
    OUTPUT_PATH,
    "fm_training_dataset.csv"
)

dataset.to_csv(output_file, index=False)

print("Dataset saved:", output_file)
print(dataset["bundle_tier"].value_counts())
print("Dataset build complete.")