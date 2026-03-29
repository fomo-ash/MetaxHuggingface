def grade(env):
    subjects = env.state_data["subjects"]

    avg_completion = sum(subjects.values()) / len(subjects)

    return max(0.0, min(1.0, avg_completion))