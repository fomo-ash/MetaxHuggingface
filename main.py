from fastapi import FastAPI
from environment import StudentLifeEnv

app = FastAPI()

env = StudentLifeEnv()


@app.get("/")
def home():
    return {
        "message": "Adaptive Exam Strategy RL Environment",
        "endpoints": [
            "/reset",
            "/step",
            "/state"
        ]
    }


@app.get("/reset")
def reset():
    state = env.reset()
    return {
        "message": "Environment reset",
        "state": state
    }


@app.post("/step")
def step(action: str):
    state, reward, done, _ = env.step(action)

    return {
        "action": action,
        "reward": reward,
        "done": done,
        "state": state
    }


@app.get("/state")
def state():
    return env.state()


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
        "max_steps": env.max_steps
    }