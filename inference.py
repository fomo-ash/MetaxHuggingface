import sys
import os
from openai import OpenAI
from environment import StudentLifeEnv

# ================== CONFIG ==================
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# ================== LOGGING ==================
def log_start():
    print("[START] task=student_exam_strategy env=StudentLifeEnv model=optimized-hybrid-agent", flush=True)

def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

# ================== OPTIMIZED FALLBACK POLICY ==================
def fallback_policy(state):
    subjects = state["subjects"]
    avg_completion = sum(subjects.values()) / len(subjects)
    weakest = min(subjects, key=subjects.get)

    # 🔥 Reduced unnecessary rest
    if state["energy"] < 0.2:
        return "rest"
    elif state["stress"] > 0.8:
        return "rest"

    # Build foundation first
    elif state["revision_level"] < 0.3:
        return "revise"

    # Improve weakest subject
    elif subjects[weakest] < 0.7:
        return f"study {weakest}"

    # 🔥 Earlier switch to high-reward phase
    elif avg_completion < 0.75:
        return "study"

    # 🔥 Maximize reward
    else:
        return "mock_test"

# ================== LLM DECISION ==================
def get_action_from_model(state):
    try:
        prompt = f"""
You are a student planning strategy agent.

Current state:
Subjects: {state['subjects']}
Energy: {state['energy']}
Stress: {state['stress']}
Revision: {state['revision_level']}

Choose ONE action:
rest, revise, study <subject>, study, mock_test

Maximize long-term score.
Output ONLY the action.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an optimal strategy agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=20
        )

        action = response.choices[0].message.content.strip()

        valid_actions = ["rest", "revise", "study", "mock_test"]
        if action in valid_actions or action.startswith("study"):
            return action

    except Exception as e:
        print(f"[DEBUG] Model error: {e}")

    # 🔥 ALWAYS FALL BACK SAFELY
    return fallback_policy(state)

# ================== MAIN ==================
def main():
    env = StudentLifeEnv()
    state = env.reset()
    
    rewards = []
    steps_taken = 0
    max_steps = env.max_steps

    log_start()

    try:
        for step in range(1, max_steps + 1):
            steps_taken = step

            # HYBRID ACTION
            action = get_action_from_model(state)

            # ENV STEP
            state, reward, done, _ = env.step(action)
            rewards.append(reward)

            # LOG
            log_step(step, action, reward, done)

            if done:
                break

        # FINAL SCORE
        final_stats = env.final_score()
        score = final_stats["scores"]["average_subject_mastery"]
        success = score >= 0.6

    except Exception as e:
        log_step(steps_taken, "error", 0.00, True, error=str(e))
        success = False
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)

# ================== RUN ==================
if __name__ == "__main__":
    main()