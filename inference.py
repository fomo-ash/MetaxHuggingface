import sys
from environment import StudentLifeEnv

def log_start():
    print("[START] task=student_exam_strategy env=StudentLifeEnv model=rule-based-baseline", flush=True)

def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def main():
    env = StudentLifeEnv()
    state = env.reset()
    
    rewards = []
    steps_taken = 0
    max_steps = env.max_steps  # 168
    
    log_start()

    try:
        for step in range(1, max_steps + 1):
            steps_taken = step
            
            # --- BASELINE RULE-BASED POLICY (from compare.py) ---
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
            # -------------------------------------------------------------

            state, reward, done, _ = env.step(action) #
            rewards.append(reward)

            # Mandatory logging
            log_step(step, action, reward, done)

            if done:
                break

        # Calculate final metrics
        final_stats = env.final_score()
        score = final_stats["scores"]["average_subject_mastery"]
        success = score >= 0.6  # Threshold for 'Good'

    except Exception as e:
        log_step(steps_taken, "error", 0.00, True, error=str(e))
        success = False
        score = 0.0
    finally:
        log_end(success, steps_taken, score, rewards)

if __name__ == "__main__":
    main()