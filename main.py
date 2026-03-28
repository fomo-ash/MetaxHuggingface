from fastapi import FastAPI
from environment import StudentLifeEnv

app = FastAPI()

env = StudentLifeEnv()

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: str):
    state, reward, done, _ = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def state():
    return env.state()