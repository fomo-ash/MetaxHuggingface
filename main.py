from fastapi import FastAPI
from pydantic import BaseModel
from environment import StudentLifeEnv
from tasks import TASKS
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Adaptive Exam Strategy RL Environment",
    description="RL environment for optimizing student exam preparation strategies",
    version="1.1"
)

env = StudentLifeEnv()


# ---------- REQUEST MODEL ----------
class ActionRequest(BaseModel):
    action: str


# ---------- HOME ----------
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


# ---------- RESET (CRITICAL FIX) ----------
@app.post("/reset")
def reset():
    state = env.reset()
    return JSONResponse(content=dict(state))


# ---------- STEP (CRITICAL FIX) ----------
@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, _ = env.step(req.action)

    return JSONResponse(content={
        "state": dict(state),
        "reward": float(reward),
        "done": bool(done)
    })


# ---------- STATE ----------
@app.get("/state")
def state():
    return JSONResponse(content=dict(env.state()))


# ---------- TASKS ----------
@app.get("/tasks")
def tasks():
    return TASKS


# ---------- FINAL SCORE ----------
@app.get("/final_score")
def final_score():
    return env.final_score()

# ---------- OPENENV RESET ----------
@app.post("/openenv/reset")
def openenv_reset():
    state = env.reset()
    return {
        "observation": state
    }


# ---------- OPENENV STEP ----------
@app.post("/openenv/step")
def openenv_step(req: ActionRequest):
    state, reward, done, _ = env.step(req.action)

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }


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