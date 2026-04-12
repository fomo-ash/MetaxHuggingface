from graders.easy import easy_grader
from graders.medium import medium_grader
from graders.hard import hard_grader

TASKS = [
    {
        "name": "easy",
        "description": "Reach average subject mastery above 0.6",
        "grader": easy_grader
    },
    {
        "name": "medium",
        "description": "Maintain low stress and good performance",
        "grader": medium_grader
    },
    {
        "name": "hard",
        "description": "Maximize efficiency under constraints",
        "grader": hard_grader
    }
]

__all__ = ["TASKS"]