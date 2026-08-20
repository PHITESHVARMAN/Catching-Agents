from pathlib import Path
from typing import List, Literal

import yaml
from pydantic import BaseModel, Field


class AgentProfile(BaseModel):
    agent_name: str
    approved_tools: List[str] = Field(default_factory=list)
    approved_data_sources: List[str] = Field(default_factory=list)
    forbidden_by_default: bool = True
    default_severity: Literal["low", "medium", "high", "critical"] = "high"
    enforcement_mode: Literal["block", "alert_only", "log_only"] = "block"
    stakeholders: List[str] = Field(default_factory=list)

    def is_tool_approved(self, tool_name: str) -> bool:
        return tool_name in self.approved_tools

    def should_block(self) -> bool:
        return self.enforcement_mode == "block"

    def should_alert(self) -> bool:
        return self.enforcement_mode in {"block", "alert_only"}


class ProfileLoader:
    def __init__(self):
        self.profiles_dir = Path(__file__).resolve().parent / "profiles"

    def load_profile(self, agent_name: str) -> AgentProfile:
        profile_path = self.profiles_dir / f"{agent_name}_profile.yaml"
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")

        with profile_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return AgentProfile(**data)


def get_profile(agent_name: str = "support_agent") -> AgentProfile:
    return ProfileLoader().load_profile(agent_name)
