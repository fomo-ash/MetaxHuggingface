from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade


def run_task(task_name, grader_fn):
    env = StudentLifeEnv()
    state = env.reset()

    total_reward = 0
    steps = 0

    print(f"[START] task={task_name}", flush=True)

    for step in range(168):
        steps += 1

        subjects = state["subjects"]
        avg_completion = sum(subjects.values()) / len(subjects)
        weakest = min(subjects, key=subjects.get)

        if state["energy"] < 0.3:
            action = "rest"
        elif state["stress"] > 0.7:
            action = "rest"
        elif state["revision_level"] < 0.3:
            action = "revise"
        elif subjects[weakest] < 0.7:
            action = f"study {weakest}"
        elif avg_completion < 0.85:
            action = "study"
        else:
            action = "mock_test"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        print(f"[STEP] step={steps} reward={reward}", flush=True)

        if done:
            break

    score = grader_fn(env)

    print(
        f"[END] task={task_name} score={score} steps={steps}",
        flush=True
    )


def main():
    run_task("easy", easy_grade)
    run_task("medium", medium_grade)
    run_task("hard", lambda env: hard_grade(0, env))


if __name__ == "__main__":
    main()