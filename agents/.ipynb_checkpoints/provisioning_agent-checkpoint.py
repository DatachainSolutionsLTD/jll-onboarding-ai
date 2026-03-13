from agents.application_pattern_learning_agent import load_fm_bundle_map
from agents.application_pattern_learning_agent import load_fm_bundle_map

def generate_provisioning_plan(selected_bundle, bundle_options):
    """
    Return application list for the selected bundle from already-built bundle options.
    """
    apps = bundle_options.get(selected_bundle, [])
    apps = list(dict.fromkeys(apps))
    return apps


if __name__ == "__main__":
    sample_bundle_options = {
        "base_bundle": ["Microsoft 365", "Chrome"],
        "standard_bundle": ["Microsoft 365", "Chrome", "Teams"],
        "advanced_bundle": ["Microsoft 365", "Chrome", "Teams", "Power BI"],
        "specialist_bundle": ["Microsoft 365", "Chrome", "Teams", "Power BI", "AutoCAD"],
    }

    apps = generate_provisioning_plan("advanced_bundle", sample_bundle_options)
    print(apps)