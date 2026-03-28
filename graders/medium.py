def grade(env):
    completion = env.state_data["syllabus_completion"]
    revision = env.state_data["revision_level"]
    score = env.state_data["mock_test_score"] / 100

    final = 0.4*completion + 0.3*revision + 0.3*score
    return max(0, min(1, final))