from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade

env = StudentLifeEnv()
state = env.reset()

for step in range(168):

    # 🧠 Smarter baseline strategy

    if state["energy"] < 0.3:
        action = "rest"

    elif state["syllabus_completion"] < 0.6:
        action = "study_new_topic"

    elif state["revision_level"] < 0.5:
        action = "revise"

    elif state["mock_test_score"] < 70:
        action = "mock_test"

    else:
        action = "revise"

    state, reward, done, _ = env.step(action)

    if done:
        break

# 📊 Compute scores
easy_score = easy_grade(env)
medium_score = medium_grade(env)
hard_score = hard_grade(env)

print("==== RESULTS ====")
print("Easy Score:", easy_score)
print("Medium Score:", medium_score)
print("Hard Score:", hard_score)