def clamp(x):
    return max(0.01, min(0.99, float(x)))


# -------- GRADERS --------

def easy_grader(scores):
    return clamp(scores.get("average_subject_mastery", 0))


def medium_grader(scores):
    avg = scores.get("average_subject_mastery", 0)
    revision = scores.get("revision_level", 0)
    return clamp(avg * (1 - revision))


def hard_grader(scores):
    return clamp(scores.get("efficiency_score", 0))


# -------- TASKS --------

TASKS = {
    "easy": {
        "goal": "Reach average subject mastery above 0.6",
        "grader": easy_grader
    },
    "medium": {
        "goal": "Maintain low stress and good performance",
        "grader": medium_grader
    },
    "hard": {
        "goal": "Maximize efficiency under constraints",
        "grader": hard_grader
    }
}