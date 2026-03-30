from fastapi import FastAPI
from pydantic import BaseModel
from environment import StudentLifeEnv
from tasks import TASKS

app = FastAPI(
    title="Adaptive Exam Strategy RL Environment",
    description="RL environment for optimizing student exam preparation strategies",
    version="1.1"
)

env = StudentLifeEnv()



class ActionRequest(BaseModel):
    action: str

class Observation(BaseModel):
    energy: float
    stress: float
    subjects: dict
    revision_level: float
    mock_test_score: float
    confidence: float
    forgetting_risk: float
    learning_efficiency: float
    exam_days_left: int


class StepResponse(BaseModel):
    action: str
    reward: float
    done: bool
    state: Observation
    reason: str
    decision_quality: str
    hints: list



@app.get("/")
def home():
    return {
        "message": "Adaptive Exam Strategy RL Environment",
        "endpoints": [
            "/reset",
            "/step",
            "/state",
            "/tasks",
            "/final_score",
            "/info"
        ]
    }

@app.get("/reset")
def reset():
    state = env.reset()
    return {
        "message": "Environment reset",
        "state": state,
        "hints": [
            "Try: study, revise, test, rest",
            "Use rest when energy is low",
            "Revise to reduce forgetting risk"
        ]
    }

@app.post("/step", response_model=StepResponse)
def step(req: ActionRequest):
    state, reward, done, info = env.step(req.action)

    return {
        "action": req.action,
        "reward": reward,
        "done": done,
        "state": state,
        "reason": info.get("reason", ""),
        "decision_quality": info.get("decision_quality", "neutral"),
        "hints": [
            "study → improve subjects",
            "revise → reduce forgetting",
            "test → evaluate performance",
            "rest → recover energy"
        ] if env.step_count < 3 else []
    }


@app.get("/state")
def state():
    return env.state()


@app.get("/tasks")
def tasks():
    return TASKS


@app.get("/final_score")
def final_score():
    return env.final_score()

@app.get("/info")
def info():
    return {
        "description": "RL environment simulating student exam preparation",
        "actions": [
            "study",
            "revise",
            "mock_test",
            "rest",
            "skip"
        ],
        "goal": "Maximize learning efficiency, retention, and performance before exam",
        "max_steps": env.max_steps
    }