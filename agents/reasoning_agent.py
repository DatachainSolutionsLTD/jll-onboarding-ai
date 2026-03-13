from openai import OpenAI

from agents.pattern_matching_agent import predict_bundle
from agents.provisioning_agent import generate_provisioning_plan
from agents.persona_normalization_agent import normalize_persona
from agents.bundle_tier_agent import build_bundle_options, select_recommended_bundle
from agents.bundle_knowledge_rag_agent import seed_bundle_knowledge, retrieve_bundle_knowledge
from agents.policy_compliance_agent import apply_policy_compliance

client = OpenAI()

ML_LABEL_MAP = {
    "FM_BASE": "Base Bundle",
    "BUNDLE_1": "Standard Bundle",
    "BUNDLE_2": "Advanced Bundle",
    "BUNDLE_3": "Specialist Bundle",
    "BUNDLE_4": "Specialist Bundle"
}

DISPLAY_BUNDLE_MAP = {
    "base_bundle": "Base Bundle",
    "standard_bundle": "Standard Bundle",
    "advanced_bundle": "Advanced Bundle",
    "specialist_bundle": "Specialist Bundle"
}


def generate_onboarding_plan(user_data):

    print("\nRunning Persona Agent...")
    normalized_persona = normalize_persona(user_data["role_title"])
    user_data["role_title"] = normalized_persona
    print("Normalized Persona:", normalized_persona)

    print("\nRunning ML Prediction Agent...")
    ml_bundle = predict_bundle(user_data)
    print("ML bundle predicted:", ml_bundle)

    print("\nRunning Bundle Tier Agent...")
    bundle_options = build_bundle_options(user_data)
    recommended_bundle = select_recommended_bundle(ml_bundle, user_data)
    print("Recommended bundle:", recommended_bundle)

    print("\nRunning Bundle Knowledge RAG Agent...")
    seed_bundle_knowledge(user_data)
    rag_result = retrieve_bundle_knowledge(recommended_bundle)
    bundle_knowledge = rag_result.get("documents", [])

    print("\nRunning Provisioning Agent...")
    applications = generate_provisioning_plan(
        recommended_bundle,
        bundle_options
    )

    print("\nRunning Policy Compliance Agent...")
    compliance_result = apply_policy_compliance(applications, user_data)
    final_applications = compliance_result["applications"]
    compliance_notes = compliance_result["compliance_notes"]

    ml_bundle_label = ML_LABEL_MAP.get(ml_bundle, ml_bundle)
    recommended_bundle_label = DISPLAY_BUNDLE_MAP.get(recommended_bundle, recommended_bundle)

    prompt = f"""
You are an enterprise IT onboarding explanation agent.

Persona: {normalized_persona}
ML Prediction: {ml_bundle_label}
Recommended Bundle: {recommended_bundle_label}

Bundle Knowledge from RAG:
{bundle_knowledge}

Final Applications:
{final_applications}

Compliance Notes:
{compliance_notes}

Explain:
1. why this persona received this recommended bundle
2. how ML prediction influenced the choice
3. how bundle knowledge was used
4. how policy compliance changed the plan
5. why the final application list is appropriate

Keep the answer professional and concise.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You explain enterprise IT onboarding decisions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    explanation = response.choices[0].message.content

    return {
        "persona": normalized_persona,
        "ml_bundle_prediction": ml_bundle,
        "recommended_bundle": recommended_bundle,
        "bundle_options": bundle_options,
        "bundle_knowledge": bundle_knowledge,
        "applications": final_applications,
        "compliance_notes": compliance_notes,
        "explanation": explanation
    }