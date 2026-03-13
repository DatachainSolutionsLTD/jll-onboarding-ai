import streamlit as st
import requests

BACKEND_URL = "https://jll-onboarding-ai-1.onrender.com/onboard_employee"

st.set_page_config(page_title="JLL AI Onboarding Portal", layout="wide")

# -------------------------------------------------------
# Enterprise UI Theme + Section Panels
# -------------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
}

body {
    background-color: white;
}

.header-banner {
    background-color: #d71920;
    height: 6px;
    width: 100%;
    margin-bottom: 20px;
}

.section-panel {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
    background-color: white;
}

.section-header {
    background-color: #fafafa;
    padding: 10px 16px;
    font-weight: 600;
    border-bottom: 1px solid #e5e7eb;
}

.section-body {
    padding: 18px;
}

.metric-label {
    font-size: 13px;
    font-weight: 500;
    color: #6b7280;
}

.metric-value {
    font-size: 22px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 12px;
}

.stButton>button {
    background-color: #d71920;
    color: white;
    border-radius: 6px;
    border: none;
    padding: 8px 18px;
    font-weight: 500;
    font-size: 14px;
}

.stButton>button:hover {
    background-color: #b5151a;
}

.bundle-box {
    padding: 8px 14px;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
    margin-right: 6px;
    font-size: 13px;
}

.agent-trace {
    background-color: #f9fafb;
    border-left: 4px solid #d71920;
    padding: 12px;
    border-radius: 6px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("JLL AI Intelligent Employee Onboarding")
st.markdown('<div class="header-banner"></div>', unsafe_allow_html=True)

st.write(
    "Persona Agent • ML Prediction Agent • Bundle Knowledge RAG Agent • "
    "Provisioning Agent • Policy Compliance Agent"
)

# -------------------------------------------------------
# DATA DEFINITIONS
# -------------------------------------------------------

REGION_COUNTRY_MAP = {
    "EMEA": ["UK", "Germany", "UAE", "France"],
    "AMER": ["US", "Canada", "Brazil"],
    "APAC": ["India", "Singapore", "Australia"]
}

JOB_ROLES = [
    "Facilities Manager",
    "Building Operations Manager",
    "Director Facilities",
    "Finance Controller",
    "HR Manager",
    "IT Operations Lead",
    "Sales Director",
    "Executive Director"
]

FUNCTION_BY_ROLE = {
    "Facilities Manager": "Facilities",
    "Building Operations Manager": "Facilities",
    "Director Facilities": "Facilities",
    "Finance Controller": "Finance",
    "HR Manager": "HR",
    "IT Operations Lead": "IT",
    "Sales Director": "Sales",
    "Executive Director": "Corporate"
}

BUNDLE_LABELS = {
    "base_bundle": "Base Bundle",
    "standard_bundle": "Standard Bundle",
    "advanced_bundle": "Advanced Bundle",
    "specialist_bundle": "Specialist Bundle"
}

ML_LABEL_MAP = {
    "FM_BASE": "Base Bundle",
    "BUNDLE_1": "Standard Bundle",
    "BUNDLE_2": "Advanced Bundle",
    "BUNDLE_3": "Specialist Bundle",
    "BUNDLE_4": "Specialist Bundle"
}

if "result" not in st.session_state:
    st.session_state.result = None

if "selected_bundle" not in st.session_state:
    st.session_state.selected_bundle = None

left, center, right = st.columns([1.2, 1.2, 1.6])

# -------------------------------------------------------
# LEFT PANEL
# -------------------------------------------------------

with left:

    st.markdown('<div class="section-panel"><div class="section-header">Employee Intake</div><div class="section-body">', unsafe_allow_html=True)

    role_title = st.selectbox("Job Title", JOB_ROLES)

    default_function = FUNCTION_BY_ROLE.get(role_title, "Corporate")

    is_manager = st.selectbox("Manager Level", ["Yes", "No"])

    function = st.selectbox(
        "Business Function",
        ["Facilities", "Finance", "HR", "IT", "Sales", "Corporate"],
        index=["Facilities", "Finance", "HR", "IT", "Sales", "Corporate"].index(default_function)
    )

    region = st.selectbox("Region", list(REGION_COUNTRY_MAP.keys()))
    country = st.selectbox("Country", REGION_COUNTRY_MAP[region])

    device_platform = st.selectbox("Device Platform", ["Windows", "Mac", "Linux"])
    ram = st.selectbox("RAM (GB)", [8, 16, 32, 64], index=1)

    installed_app_count = st.slider("Installed Applications", 5, 60, 25)

    payload = {
        "role_title": role_title,
        "is_manager": is_manager,
        "function": function,
        "region": region,
        "country": country,
        "device_platform": device_platform,
        "ram": int(ram),
        "installed_app_count": int(installed_app_count)
    }

    if st.button("Generate Recommendation"):

        with st.spinner("Running AI agents and generating recommendation..."):

            try:

                response = requests.post(
                    BACKEND_URL,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.result = result
                    st.session_state.selected_bundle = result.get("recommended_bundle")

                    st.success("Recommendation generated")

                else:
                    st.error("Backend error")

            except Exception as e:
                st.error("Connection error")
                st.write(e)

    st.markdown('</div></div>', unsafe_allow_html=True)

result = st.session_state.result

# -------------------------------------------------------
# CENTER PANEL
# -------------------------------------------------------

if result:

    with center:

        st.markdown('<div class="section-panel"><div class="section-header">Bundle Recommendation Engine</div><div class="section-body">', unsafe_allow_html=True)

        persona = result.get("persona")

        ml_prediction = ML_LABEL_MAP.get(
            result.get("ml_bundle_prediction"),
            result.get("ml_bundle_prediction")
        )

        recommended_bundle_key = result.get("recommended_bundle")

        recommended_bundle = BUNDLE_LABELS.get(
            recommended_bundle_key,
            recommended_bundle_key
        )

        st.markdown(f'<div class="metric-label">Persona</div><div class="metric-value">{persona}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">ML Prediction</div><div class="metric-value">{ml_prediction}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Recommended Bundle</div><div class="metric-value">{recommended_bundle}</div>', unsafe_allow_html=True)

        bundle_options = result.get("bundle_options", {})
        bundle_list = list(bundle_options.keys())

        selected_bundle = st.selectbox(
            "Compare Bundles",
            bundle_list,
            index=bundle_list.index(st.session_state.selected_bundle)
            if st.session_state.selected_bundle in bundle_list else 0,
            format_func=lambda x: BUNDLE_LABELS.get(x, x)
        )

        st.session_state.selected_bundle = selected_bundle

        apps = bundle_options.get(selected_bundle, [])

        st.markdown(
            f'<div class="metric-label">Bundle Size</div><div class="metric-value">{len(apps)} Applications</div>',
            unsafe_allow_html=True
        )

        with st.expander("View bundle contents", expanded=False):

            if len(apps) > 80:
                st.info(f"Showing first 80 of {len(apps)} applications for performance")

            for app in apps[:80]:
                st.write("•", app)

        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-panel"><div class="section-header">Bundle Intelligence Layer</div><div class="section-body">', unsafe_allow_html=True)

        for doc in result.get("bundle_knowledge", []):
            st.write(doc)

        st.markdown('</div></div>', unsafe_allow_html=True)

# -------------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------------

if result:

    with right:

        st.markdown('<div class="section-panel"><div class="section-header">Provisioning Plan & Policy Compliance</div><div class="section-body">', unsafe_allow_html=True)

        if st.button("Create Provisioning Plan"):

            with st.spinner("Generating provisioning plan..."):

                try:

                    override_payload = payload.copy()
                    override_payload["selected_bundle"] = st.session_state.selected_bundle

                    response = requests.post(
                        BACKEND_URL,
                        json=override_payload,
                        timeout=60
                    )

                    if response.status_code == 200:

                        final = response.json()

                        with st.expander("Applications to Install", expanded=False):

                            apps = final.get("applications", [])

                            if len(apps) > 100:
                                st.info(f"Showing first 100 of {len(apps)} applications")

                            for app in apps[:100]:
                                st.write("•", app)

                        st.markdown("### Policy Compliance Notes")

                        for note in final.get("compliance_notes", []):
                            st.write("•", note)

                        st.markdown("### AI Decision Rationale")

                        st.write(final.get("explanation"))

                        st.markdown("### Agent Execution Trace")

                        st.markdown("""
                        <div class="agent-trace">

                        ✔ Persona Agent → Persona identified<br>
                        ✔ ML Prediction Agent → Bundle predicted<br>
                        ✔ Bundle Knowledge Agent → Retrieved bundle catalog<br>
                        ✔ Provisioning Agent → Generated provisioning plan<br>
                        ✔ Policy Compliance Agent → Applied regional policy

                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.error("Backend error")

                except Exception as e:
                    st.error("Connection error")
                    st.write(e)

        st.markdown('</div></div>', unsafe_allow_html=True)