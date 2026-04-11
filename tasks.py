TASKS = {
    "easy": {
        "goal": "Reach average subject mastery above 0.6",
        "grader": lambda scores: min(max(scores.get("average_subject_mastery", 0.0), 0.01), 0.99)
    },

    "medium": {
        "goal": "Maintain low stress (<0.5) while achieving good performance",
        "grader": lambda scores: min(
            max(
                (1 - scores.get("stress_level", 1.0)) * scores.get("average_subject_mastery", 0.0),
                0.01
            ),
            0.99
        )
    },

    "hard": {
        "goal": "Maximize performance under constraints (high score + balanced state)",
        "grader": lambda scores: min(
            max(scores.get("efficiency_score", 0.0), 0.01),
            0.99
        )
    }
}