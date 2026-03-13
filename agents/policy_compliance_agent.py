def apply_policy_compliance(applications, user_profile):
    """
    Apply policy-based compliance rules to final provisioning plan.
    """
    region = str(user_profile.get("region", "")).upper()
    device_platform = str(user_profile.get("device_platform", "")).lower()
    ram = int(user_profile.get("ram", 0) or 0)

    final_apps = applications[:]
    compliance_notes = []

    windows_only_markers = [
        "dell",
        "realtek",
        "displaylink",
        "windows desktop runtime",
        "visual c++"
    ]

    heavy_app_markers = [
        "autocad",
        "tableau",
        "power bi",
        "visual studio code"
    ]

    if device_platform == "mac":
        before = len(final_apps)
        final_apps = [
            app for app in final_apps
            if not any(marker in app.lower() for marker in windows_only_markers)
        ]
        if len(final_apps) != before:
            compliance_notes.append("Removed Windows-only applications for Mac device.")

    if ram < 16:
        before = len(final_apps)
        final_apps = [
            app for app in final_apps
            if not any(marker in app.lower() for marker in heavy_app_markers)
        ]
        if len(final_apps) != before:
            compliance_notes.append("Removed heavy applications for lower-RAM device.")

    if region == "EMEA":
        final_apps.append("EMEA Regional Compliance Pack")
        compliance_notes.append("Added EMEA compliance pack.")
    elif region == "AMER":
        final_apps.append("AMER Regional Compliance Pack")
        compliance_notes.append("Added AMER compliance pack.")
    elif region == "APAC":
        final_apps.append("APAC Regional Compliance Pack")
        compliance_notes.append("Added APAC compliance pack.")

    final_apps = list(dict.fromkeys(final_apps))

    return {
        "applications": final_apps,
        "compliance_notes": compliance_notes
    }