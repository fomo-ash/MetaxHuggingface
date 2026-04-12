def medium_grader(env):
    subjects = env.state_data["subjects"]

    avg_completion = sum(subjects.values()) / len(subjects)
    revision = env.state_data["revision_level"]

    score = 0.6 * avg_completion + 0.4 * revision
    return max(0.0, min(1.0, score))