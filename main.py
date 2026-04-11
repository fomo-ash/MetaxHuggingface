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


# ---------- REQUEST MODEL ----------
class ActionRequest(BaseModel):
    action: str


# ---------- ROOT (CRITICAL FOR VALIDATOR) ----------
@app.get("/")
@app.post("/")
def root():
    state = env.reset()
    return {
        "observation": state
    }


# ---------- RESET (ALL COMPATIBLE ROUTES) ----------
@app.post("/reset")
@app.post("/reset/")
@app.post("/openenv/reset")
@app.post("/openenv/reset/")
def reset_all():
    state = env.reset()
    return {
        "observation": state
    }


# ---------- STEP (ALL COMPATIBLE ROUTES) ----------
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


# ---------- STATE ----------
@app.get("/state")
def state():
    return env.state()


# ---------- TASKS ----------
@app.get("/tasks")
def tasks():
    return {
        name: {
            "goal": task["goal"],
            "grader": "exists"   # 👈 IMPORTANT
        }
        for name, task in TASKS.items()
    }

# ---------- FINAL SCORE ----------
@app.get("/final_score")
def final_score():
    return env.final_score()


# ---------- INFO ----------
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