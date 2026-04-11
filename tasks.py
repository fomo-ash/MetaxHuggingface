def clamp(x):
    return max(0.01, min(0.99, float(x)))


TASKS = {

    "easy": {
        "goal": "Reach average subject mastery above 0.6",

        "grader": lambda scores: clamp(
            scores.get("average_subject_mastery", 0)
        )
    },

    "medium": {
        "goal": "Maintain low stress and good performance",

        "grader": lambda scores: clamp(
            scores.get("average_subject_mastery", 0) *
            (1 - scores.get("revision_level", 0))
        )
    },

    "hard": {
        "goal": "Maximize efficiency under constraints",

        "grader": lambda scores: clamp(
            scores.get("efficiency_score", 0)
        )
    }
}