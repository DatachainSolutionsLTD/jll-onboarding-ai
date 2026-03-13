import copy
from agents.application_pattern_learning_agent import load_fm_bundle_map

TIER_ORDER = [
    "base_bundle",
    "standard_bundle",
    "advanced_bundle",
    "specialist_bundle",
]

ML_TO_TIER = {
    "FM_BASE": "base_bundle",
    "BUNDLE_1": "standard_bundle",
    "BUNDLE_2": "advanced_bundle",
    "BUNDLE_3": "specialist_bundle",
    "BUNDLE_4": "specialist_bundle",
}


def dedupe_keep_order(items):
    return list(dict.fromkeys(items))


def limit_bundle_size(bundle_name, apps):

    limits = {
        "base_bundle": 20,
        "standard_bundle": 35,
        "advanced_bundle": 50,
        "specialist_bundle": 70
    }

    max_apps = limits.get(bundle_name, 40)

    return apps[:max_apps]


def build_bundle_options(user_profile=None):

    fm_map = load_fm_bundle_map()

    base = fm_map.get("FM_BASE", [])
    b1 = fm_map.get("BUNDLE_1", [])
    b2 = fm_map.get("BUNDLE_2", [])
    b3 = fm_map.get("BUNDLE_3", [])
    b4 = fm_map.get("BUNDLE_4", [])

    bundle_options = {
        "base_bundle": dedupe_keep_order(base),
        "standard_bundle": dedupe_keep_order(base + b1),
        "advanced_bundle": dedupe_keep_order(base + b1 + b2),
        "specialist_bundle": dedupe_keep_order(base + b1 + b2 + b3 + b4),
    }

    # limit bundle size
    for key in bundle_options:
        bundle_options[key] = limit_bundle_size(key, bundle_options[key])

    return apply_context_rules(bundle_options, user_profile or {})


def tier_index(tier_name):
    return TIER_ORDER.index(tier_name)


def tier_from_index(idx):
    idx = max(0, min(idx, len(TIER_ORDER) - 1))
    return TIER_ORDER[idx]


def map_ml_bundle_to_exposed_tier(ml_bundle):
    return ML_TO_TIER.get(ml_bundle, "standard_bundle")


def select_recommended_bundle(ml_bundle, user_profile):

    persona = user_profile.get("role_title", "")

    persona_defaults = {
        "HR Business Partner": "standard_bundle",
        "Finance Manager": "advanced_bundle",
        "Facilities Manager": "advanced_bundle",
        "IT Operations": "specialist_bundle",
        "Sales Executive": "standard_bundle",
        "Executive Leadership": "advanced_bundle"
    }

    if persona in persona_defaults:
        return persona_defaults[persona]

    return map_ml_bundle_to_exposed_tier(ml_bundle)


def apply_context_rules(bundle_options, user_profile):

    options = copy.deepcopy(bundle_options)

    device_platform = str(user_profile.get("device_platform", "")).lower()
    region = str(user_profile.get("region", "")).upper()
    ram = int(user_profile.get("ram", 0))

    windows_only_markers = [
        "dell",
        "realtek",
        "displaylink",
        "windows desktop runtime",
        "visual c++",
    ]

    heavy_app_markers = [
        "visual studio code",
        "tableau",
        "power bi",
        "autocad",
    ]

    for tier_name, apps in options.items():

        filtered = apps[:]

        if device_platform == "mac":
            filtered = [
                app for app in filtered
                if not any(marker in app.lower() for marker in windows_only_markers)
            ]

        if ram < 16:
            filtered = [
                app for app in filtered
                if not any(marker in app.lower() for marker in heavy_app_markers)
            ]

        if region == "EMEA":
            filtered.append("EMEA Regional Compliance Pack")
        elif region == "US":
            filtered.append("US Regional Compliance Pack")
        elif region == "APAC":
            filtered.append("APAC Regional Compliance Pack")

        options[tier_name] = dedupe_keep_order(filtered)

    return options