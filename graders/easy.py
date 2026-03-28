def grade(env):
    return min(1.0, env.state_data["syllabus_completion"])