def easy_grader(env, total_reward=0):
    subjects = env.state_data["subjects"]
    avg = sum(subjects.values()) / len(subjects)
    return max(0.0, min(1.0, avg))