from environment import StudentLifeEnv

def main():
    print("[START] task=test", flush=True)

    env = StudentLifeEnv()
    state = env.reset()

    total_reward = 0

    for step in range(5):  # keep small for safety
        action = "study"
        state, reward, done, _ = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step+1} reward={reward}", flush=True)

    print(f"[END] task=test score={total_reward} steps=5", flush=True)


if __name__ == "__main__":
    main()