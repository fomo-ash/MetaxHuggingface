from graders.easy import easy_grader
from graders.medium import medium_grader
from graders.hard import hard_grader


TASKS = [
    {
        "name": "easy",
        "goal": "Reach average subject mastery above 0.6",
        "grader_fn": easy_grader
    },
    {
        "name": "medium",
        "goal": "Maintain low stress and good performance",
        "grader_fn": medium_grader
    },
    {
        "name": "hard",
        "goal": "Maximize efficiency under constraints",
        "grader_fn": hard_grader
    }
]