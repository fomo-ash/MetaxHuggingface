import random
import statistics

from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade


NUM_EPISODES = 10   # increase for stability

ACTIONS = [
    "study",
    "study math",
    "study physics",
    "study chemistry",
    "revise",
    "mock_test",
    "rest",
    "skip"
]


def baseline_policy(state):

    subjects = state["subjects"]
    avg_completion = sum(subjects.values()) / len(subjects)
    weakest = min(subjects, key=subjects.get)

    if state["energy"] < 0.3:
        return "rest"

    elif state["stress"] > 0.7:
        return "rest"

    elif state["revision_level"] < 0.3:
        return "revise"

    elif subjects[weakest] < 0.7:
        return f"study {weakest}"

    elif avg_completion < 0.85:
        return "study"

    else:
        return "mock_test"


def random_policy(state):
    return random.choice(ACTIONS)


def run_agent(policy_fn):

    rewards = []
    easy_scores = []
    medium_scores = []
    hard_scores = []

    for seed in range(NUM_EPISODES):

        random.seed(seed)

        env = StudentLifeEnv()
        state = env.reset()

        total_reward = 0

        for step in range(168):

            action = policy_fn(state)

            state, reward, done, _ = env.step(action)
            total_reward += reward

            if done:
                break

        rewards.append(total_reward)
        easy_scores.append(easy_grade(env))
        medium_scores.append(medium_grade(env))
        hard_scores.append(hard_grade(total_reward, env))

    return {
        "reward": statistics.median(rewards),
        "easy": statistics.median(easy_scores),
        "medium": statistics.median(medium_scores),
        "hard": statistics.median(hard_scores)
    }


def print_agent(name, data):

    print(f"\n{name}")
    print("----------------")
    print(f"Reward : {data['reward']:.2f}")
    print(f"Easy   : {data['easy']:.2f}")
    print(f"Medium : {data['medium']:.2f}")
    print(f"Hard   : {data['hard']:.2f}")


def main():

    print("\nRunning Baseline Agent...")
    baseline = run_agent(baseline_policy)

    print("Running Random Agent...")
    random_agent = run_agent(random_policy)

    print("\n==============================")
    print("Baseline vs Random Comparison")
    print("==============================")

    print_agent("Baseline Agent", baseline)
    print_agent("Random Agent", random_agent)

    print("\n==============================")
    print("Difference (Baseline - Random)")
    print("==============================")

    print(f"Reward : {baseline['reward'] - random_agent['reward']:.2f}")
    print(f"Easy   : {baseline['easy'] - random_agent['easy']:.2f}")
    print(f"Medium : {baseline['medium'] - random_agent['medium']:.2f}")
    print(f"Hard   : {baseline['hard'] - random_agent['hard']:.2f}")


if __name__ == "__main__":
    main()