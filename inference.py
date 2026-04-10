import sys
import os
import time
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
from environment import StudentLifeEnv

# ================== CONFIG ==================
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

# Initialize client with a check for API_KEY
client = None
if API_KEY and OpenAI:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except Exception:
        client = None

# ================== LOGGING ==================
# CRITICAL: These must be printed to stdout and flushed immediately
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

    if state["energy"] < 0.2:
        return "rest"
    elif state["stress"] > 0.8:
        return "rest"
    elif state["revision_level"] < 0.3:
        return "revise"
    elif subjects[weakest] < 0.7:
        return f"study {weakest}"
    elif avg_completion < 0.75:
        return "study"
    else:
        return "mock_test"

# ================== ACTION SELECTION ==================
def get_action_from_model(state):
    if not client:
        return fallback_policy(state)
        
    try:
        prompt = f"Subjects: {state['subjects']}, Energy: {state['energy']}, Stress: {state['stress']}. Choose: rest, revise, study, or mock_test."
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            timeout=5.0 # Prevent hanging
        )
        action = response.choices[0].message.content.strip().lower()
        valid_actions = ["rest", "revise", "study", "mock_test"]
        if any(v in action for v in valid_actions):
            # Clean up the action string to match env expectations
            for v in valid_actions:
                if v in action: return v
    except Exception:
        pass
    return fallback_policy(state)

# ================== MAIN ==================
def main():
    env = StudentLifeEnv()
    state = env.reset()
    rewards = []
    steps_taken = 0
    max_steps = env.max_steps

    log_start() # Mandatory

    try:
        for step in range(1, max_steps + 1):
            steps_taken = step
            action = get_action_from_model(state)
            
            state, reward, done, _ = env.step(action)
            rewards.append(reward)
            log_step(step, action, reward, done)

            if done:
                break

        final_stats = env.final_score()
        score = final_stats["scores"]["average_subject_mastery"]
        success = score >= 0.6

    except Exception as e:
        log_step(steps_taken, "error", 0.0, True, error=str(e))
        success, score = False, 0.0
    finally:
        log_end(success, steps_taken, score, rewards) # Mandatory

if __name__ == "__main__":
    main()