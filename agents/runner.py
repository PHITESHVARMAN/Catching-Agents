from agents.tools import get_tool


class SupportAgentRunner:
    def __init__(self, profile, callback):
        self.profile = profile
        self.callback = callback

    def run(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()
        steps = []
        blocked = False

        requested_tools = []

        if any(w in prompt_lower for w in ["return", "shipping", "refund", "faq", "policy"]):
            requested_tools.append(("search_faq", {"query": prompt}))

        if "email" in prompt_lower or "send" in prompt_lower:
            requested_tools.append(
                ("send_email", {"to": "customer@example.com", "subject": "Info", "body": "Here is the info"})
            )

        if "customer id" in prompt_lower or "look up" in prompt_lower:
            requested_tools.append(("access_customer_db", {"customer_id": "4521"}))

        if "delete" in prompt_lower or "remove" in prompt_lower:
            requested_tools.append(("delete_record", {"record_id": "REC-123"}))

        if "shell" in prompt_lower or "command" in prompt_lower:
            requested_tools.append(("execute_shell", {"command": "dir"}))

        if not requested_tools:
            return {
                "response": "I could not identify an action for that request.",
                "violations": self.callback.violations,
                "steps": [],
                "blocked": False,
            }

        for tool_name, tool_input in requested_tools:
            violation = self.callback.before_tool_call(tool_name, tool_input)

            if violation and self.profile.should_block():
                blocked = True
                steps.append({"tool": tool_name, "status": "blocked", "input": tool_input})
                continue

            tool_fn = get_tool(tool_name)
            output = tool_fn(**tool_input)

            steps.append({"tool": tool_name, "status": "executed", "input": tool_input, "output": output})

        response = "The request was blocked by governance policy." if blocked else "Request completed successfully."

        return {
            "response": response,
            "violations": self.callback.violations,
            "steps": steps,
            "blocked": blocked,
        }
