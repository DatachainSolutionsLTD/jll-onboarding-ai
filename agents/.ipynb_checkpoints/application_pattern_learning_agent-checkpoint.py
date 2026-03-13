import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
BUNDLE_FILE = os.path.join(RAW_DATA_PATH, "FM_Application_Bundles.xlsx")


def load_fm_bundle_map():
    """
    Reads the FM_Application_Bundles.xlsx workbook and returns the raw bundle columns.

    Output:
    {
        "FM_BASE": [...],
        "BUNDLE_1": [...],
        "BUNDLE_2": [...],
        "BUNDLE_3": [...],
        "BUNDLE_4": [...]
    }
    """

    print("Loading FM application bundle definitions...")

    df = pd.read_excel(
        BUNDLE_FILE,
        sheet_name="Application Bundles",
        header=None
    )

    # Data starts after the repeated header rows
    data_rows = df.iloc[3:].reset_index(drop=True)

    # Workbook layout:
    # FM_BASE   -> col 0
    # BUNDLE_1  -> col 3
    # BUNDLE_2  -> col 6
    # BUNDLE_3  -> col 9
    # BUNDLE_4  -> col 12
    col_map = {
        "FM_BASE": 0,
        "BUNDLE_1": 3,
        "BUNDLE_2": 6,
        "BUNDLE_3": 9,
        "BUNDLE_4": 12
    }

    bundle_map = {}

    for bundle_name, col_idx in col_map.items():
        apps = (
            data_rows.iloc[:, col_idx]
            .dropna()
            .astype(str)
            .map(str.strip)
            .tolist()
        )

        apps = [
            app for app in apps
            if app and app.lower() != "application name"
        ]

        bundle_map[bundle_name] = apps

    print("Bundle map loaded successfully")
    for bundle_name, apps in bundle_map.items():
        print(f"{bundle_name}: {len(apps)} apps")

    return bundle_map