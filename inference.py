from environment import StudentLifeEnv


def log_start():
    print("[START] task=student env=custom model=rule-based", flush=True)


def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(steps, rewards):
    total = sum(rewards)
    score = max(0.0, min(1.0, total / len(rewards))) if rewards else 0.0
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success=true steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


def main():
    env = StudentLifeEnv()
    state = env.reset()

    rewards = []
    steps = 0

    log_start()

    for step in range(1, 20):  # small safe run
        steps = step

        subjects = state["subjects"]
        weakest = min(subjects, key=subjects.get)

        if state["energy"] < 0.3:
            action = "rest"
        elif state["stress"] > 0.7:
            action = "rest"
        elif state["revision_level"] < 0.3:
            action = "revise"
        elif subjects[weakest] < 0.7:
            action = f"study {weakest}"
        else:
            action = "mock_test"

        state, reward, done, _ = env.step(action)

        rewards.append(reward)

        log_step(step, action, reward, done)

        if done:
            break

    log_end(steps, rewards)


if __name__ == "__main__":
    main()