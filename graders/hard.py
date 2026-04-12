def hard_grader(env, total_reward=0):
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

    return max(0.0, min(1.0, score))