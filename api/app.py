from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.reasoning_agent import generate_onboarding_plan
from agents.provisioning_agent import generate_provisioning_plan


app = FastAPI(
    title="JLL AI Onboarding Service",
    description="Agentic AI system for onboarding bundle prediction, provisioning, RAG, and compliance",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmployeeProfile(BaseModel):
    role_title: str
    is_manager: str
    function: str
    region: str
    country: str
    device_platform: str
    ram: int
    installed_app_count: int
    selected_bundle: Optional[str] = None


@app.get("/")
def home():
    return {
        "message": "JLL AI Onboarding API is running",
        "version": "3.0"
    }


@app.post("/onboard_employee")
def onboard_employee(profile: EmployeeProfile):
    user_data = profile.dict()
    result = generate_onboarding_plan(user_data)

    if profile.selected_bundle:
        bundle_options = result.get("bundle_options", {})
        applications = generate_provisioning_plan(
            profile.selected_bundle,
            bundle_options
        )
        result["recommended_bundle"] = profile.selected_bundle
        result["applications"] = applications

    return result