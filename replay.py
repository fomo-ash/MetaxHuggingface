import json
from datetime import datetime

from environment import StudentLifeEnv
from graders.easy import grade as easy_grade
from graders.medium import grade as medium_grade
from graders.hard import grade as hard_grade


def run_episode():

    env = StudentLifeEnv()
    state = env.reset()

    trajectory = []
    total_reward = 0

    for step in range(168):

        subjects = state["subjects"]
        avg_completion = sum(subjects.values()) / len(subjects)
        weakest = min(subjects, key=subjects.get)

        # Same baseline policy (reuse inference logic)
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

        next_state, reward, done, _ = env.step(action)

        # log trajectory step
        trajectory.append({
            "step": step,
            "action": action,
            "reward": reward,
            "state": next_state
        })

        total_reward += reward
        state = next_state

        if done:
            break

    # Final Scores
    easy_score = easy_grade(env)
    medium_score = medium_grade(env)
    hard_score = hard_grade(total_reward, env)

    # Summary
    summary = {
        "total_steps": len(trajectory),
        "total_reward": total_reward,
        "easy_score": easy_score,
        "medium_score": medium_score,
        "hard_score": hard_score,
        "timestamp": datetime.now().isoformat()
    }

    output = {
        "summary": summary,
        "trajectory": trajectory
    }

    # Save JSON
    with open("episode_1.json", "w") as f:
        json.dump(output, f, indent=2)

    # Print summary
    print("\n==============================")
    print("Episode Replay Summary")
    print("==============================")

    print(f"Steps        : {summary['total_steps']}")
    print(f"Total Reward : {summary['total_reward']:.2f}")
    print(f"Easy Score   : {summary['easy_score']:.2f}")
    print(f"Medium Score : {summary['medium_score']:.2f}")
    print(f"Hard Score   : {summary['hard_score']:.2f}")

    print("\nSaved: episode_1.json")


if __name__ == "__main__":
    run_episode()