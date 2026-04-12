from graders.easy import easy_grader
from graders.medium import medium_grader
from graders.hard import hard_grader

def clamp(x):
    return max(0.01, min(0.99, float(x)))


def easy_grader(env):
    subjects = env.state_data["subjects"]
    avg = sum(subjects.values()) / len(subjects)
    return clamp(avg)


def medium_grader(env):
    subjects = env.state_data["subjects"]
    avg = sum(subjects.values()) / len(subjects)
    revision = env.state_data["revision_level"]
    return clamp(0.6 * avg + 0.4 * revision)


def hard_grader(env):
    subjects = env.state_data["subjects"]

    values = list(subjects.values())
    balance = 1 - (max(values) - min(values))

    avg = sum(values) / len(values)
    mock = env.state_data["mock_test_score"] / 100
    confidence = env.state_data["confidence"]
    stress_penalty = 1 - env.state_data["stress"]

    score = (
        0.25 * avg +
        0.2 * balance +
        0.25 * mock +
        0.2 * confidence +
        0.1 * stress_penalty
    )

    return clamp(score)


TASKS = [
    {"name": "easy", "goal": "Reach average subject mastery above 0.6", "grader_fn": easy_grader},
    {"name": "medium", "goal": "Maintain low stress and good performance", "grader_fn": medium_grader},
    {"name": "hard", "goal": "Maximize efficiency under constraints", "grader_fn": hard_grader},
]