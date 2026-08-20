from datetime import datetime


class PolicyEnforcer:
    def check_tool(self, tool_name: str, profile) -> dict | None:
        if profile.is_tool_approved(tool_name):
            return None

        return {
            "agent_name": profile.agent_name,
            "tool_name": tool_name,
            "violation_type": "policy_breach",
            "severity": profile.default_severity,
            "description": f"Tool '{tool_name}' is not approved",
            "blocked": profile.should_block(),
            "detected_at": datetime.now().isoformat(),
        }
