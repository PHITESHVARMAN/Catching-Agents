from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.runner import SupportAgentRunner
from governance.callback_handler import GovernanceCallbackHandler
from governance.policy_enforcer import PolicyEnforcer
from governance.profile_loader import get_profile
from governance.response_handler import ResponseHandler

router = APIRouter()


class AgentRunRequest(BaseModel):
    prompt: str
    agent_name: str = "support_agent"


@router.post("/run")
def run_agent(request: AgentRunRequest) -> dict:
    try:
        # 1. Load the profile.
        profile = get_profile(request.agent_name)

        # 2. Create the DB + SMTP-capable response handler.
        # It reads DB_CONFIG and EMAIL_CONFIG from governance/config.py.
        response_handler = ResponseHandler(profile=profile)

        # 3. Create monitor/enforcer with the response handler.
        callback = GovernanceCallbackHandler(
            profile=profile,
            policy_enforcer=PolicyEnforcer(),
            response_handler=response_handler,
        )

        # 4. Run the agent.
        runner = SupportAgentRunner(profile, callback)
        return runner.run(request.prompt)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))