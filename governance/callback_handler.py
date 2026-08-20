from datetime import datetime


class GovernanceCallbackHandler:
    def __init__(self, profile, policy_enforcer, response_handler):
        self.profile = profile
        self.policy_enforcer = policy_enforcer
        self.response_handler = response_handler
        self.violations = []
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")

    def before_tool_call(self, tool_name: str, tool_input: dict) -> dict | None:
        violation = self.policy_enforcer.check_tool(tool_name, self.profile)

        if violation is None:
            return None

        violation["session_id"] = self.session_id
        violation["tool_input"] = tool_input

        self.violations.append(violation)

        # This is the important line:
        # It saves to DB and sends the SMTP email immediately.
        self.response_handler.handle_violation(violation)

        return violation