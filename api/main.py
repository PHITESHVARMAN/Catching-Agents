from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.agents import router as agents_router

app = FastAPI(title="AI Agent Governance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(agents_router, prefix="/api/agents", tags=["agents"])
