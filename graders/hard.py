def grade(env):
    completion = env.state_data["syllabus_completion"]
    revision = env.state_data["revision_level"]
    score = env.state_data["mock_test_score"] / 100
    stress_penalty = 1 - env.state_data["stress"]

    final = 0.3*completion + 0.3*revision + 0.3*score + 0.1*stress_penalty
    return max(0, min(1, final))