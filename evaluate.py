import json
import statistics
from datetime import datetime

from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade


NUM_RUNS = 8   # 5–10 runs recommended


def run_episode():
    env = StudentLifeEnv()
    state = env.reset()

    total_reward = 0

    for step in range(168):

        subjects = state["subjects"]
        avg_completion = sum(subjects.values()) / len(subjects)
        weakest = min(subjects, key=subjects.get)

        # Same baseline policy as inference.py
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

        if done:
            break

    # grading
    easy_score = easy_grade(env)
    medium_score = medium_grade(env)
    hard_score = hard_grade(total_reward, env)

    return {
        "total_reward": total_reward,
        "easy": easy_score,
        "medium": medium_score,
        "hard": hard_score
    }


def main():

    print("\n==============================")
    print("Adaptive Exam Strategy Benchmark")
    print("==============================\n")

    results = []

    for i in range(NUM_RUNS):
        result = run_episode()
        results.append(result)

        print(
            f"Run {i+1} | "
            f"Reward: {result['total_reward']:.2f} | "
            f"Easy: {result['easy']:.2f} | "
            f"Medium: {result['medium']:.2f} | "
            f"Hard: {result['hard']:.2f}"
        )

    # averages
    avg_reward = statistics.mean(r["total_reward"] for r in results)
    avg_easy = statistics.mean(r["easy"] for r in results)
    avg_medium = statistics.mean(r["medium"] for r in results)
    avg_hard = statistics.mean(r["hard"] for r in results)

    print("\n==============================")
    print("AVERAGE RESULTS")
    print("==============================")

    print(f"Average Reward : {avg_reward:.2f}")
    print(f"Average Easy   : {avg_easy:.2f}")
    print(f"Average Medium : {avg_medium:.2f}")
    print(f"Average Hard   : {avg_hard:.2f}")

    # save json
    output = {
        "runs": results,
        "average": {
            "reward": avg_reward,
            "easy": avg_easy,
            "medium": avg_medium,
            "hard": avg_hard
        },
        "timestamp": datetime.now().isoformat()
    }

    with open("benchmark_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nSaved benchmark_results.json")


if __name__ == "__main__":
    main()