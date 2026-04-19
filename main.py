from fastapi import FastAPI
from pydantic import BaseModel
from environment import StudentLifeEnv
from tasks import TASKS

app = FastAPI(
    title="Adaptive Exam Strategy RL Environment",
    description="RL environment for optimizing student exam preparation strategies",
    version="1.2"
)

env = StudentLifeEnv()


class ActionRequest(BaseModel):
    action: str


@app.get("/")
@app.post("/")
def root():
    state = env.reset()
    return {
        "observation": state
    }


@app.post("/reset")
@app.post("/reset/")
@app.post("/openenv/reset")
@app.post("/openenv/reset/")
def reset_all():
    state = env.reset()
    return {
        "observation": state
    }


@app.post("/step")
@app.post("/step/")
@app.post("/openenv/step")
@app.post("/openenv/step/")
def step_all(req: ActionRequest):
    state, reward, done, _ = env.step(req.action)

    return {
        "observation": state,
        "reward": float(reward),
        "done": bool(done),
        "info": {}
    }


@app.get("/state")
def state():
    return env.state()


@app.get("/tasks")
def tasks():
    return {
        task["name"]: {
            "goal": task["goal"],
            "grader_fn": True
        }
        for task in TASKS
    }


@app.get("/final_score")
def final_score():
    return env.final_score()


@app.get("/info")
def info():
    return {
        "description": "RL environment simulating student exam preparation",
        "actions": [
            "study_new_topic",
            "revise",
            "mock_test",
            "rest",
            "skip"
        ],
        "goal": "Maximize learning efficiency, retention, and performance before exam",
        "max_steps": env.max_steps
    }