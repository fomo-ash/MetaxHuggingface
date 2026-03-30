from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade

env = StudentLifeEnv()
state = env.reset()

total_reward = 0

for step in range(168):

    subjects = state["subjects"]
    avg_completion = sum(subjects.values()) / len(subjects)

    weakest = min(subjects, key=subjects.get)

    if state["energy"] < 0.3:
        action = "rest"

    elif state["stress"] > 0.7:
        action = "rest"

    elif state["revision_level"] < 0.3:
        action = "revise"

    elif subjects[weakest] < 0.7:
        action = f"study {weakest}"   

    elif avg_completion < 0.85:
        action = "study"

    else:
        action = "mock_test"

    state, reward, done, _ = env.step(action)
    total_reward += reward

    if done:
        break


easy_score = easy_grade(env)
medium_score = medium_grade(env)
hard_score = hard_grade(total_reward, env)

print("==== RESULTS ====")
print("Easy Score:", easy_score)
print("Medium Score:", medium_score)
print("Hard Score:", hard_score)