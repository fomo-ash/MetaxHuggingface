import os
from openai import OpenAI
from environment import StudentLifeEnv

# 1. SETUP VARIABLES - Mandatory Checklist Requirements
# Defaults are set ONLY for API_BASE_URL and MODEL_NAME
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
# Do NOT set a default for HF_TOKEN
API_KEY = os.getenv("HF_TOKEN") 

def main():
    # 2. INITIALIZE CLIENT
    # All LLM calls must use this client
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    env = StudentLifeEnv()
    state = env.reset()
    rewards = []
    
    # 3. [START] LOG - Mandatory Format
    print(f"[START] task=student_exam_strategy env=StudentLifeEnv model={MODEL_NAME}", flush=True)

    try:
        # Loop matches max_steps from environment
        for step in range(1, env.max_steps + 1):
            # 4. MANDATORY LLM CALL using the client
            prompt = f"State: {state}. Actions: [study_new_topic, revise, mock_test, rest, skip]."
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=15
            )
            action = response.choices[0].message.content.strip().lower()

            # 5. ENVIRONMENT STEP
            state, reward, done, _ = env.step(action)
            rewards.append(reward)

            # 6. [STEP] LOG - Mandatory Format (flush=True)
            print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)

            if done:
                break

        # 7. FINAL SCORING
        final_stats = env.final_score()
        score = final_stats["scores"]["average_subject_mastery"]
        success = score >= 0.6

    except Exception as e:
        # Log error in STEP format if something fails
        print(f"[STEP] step=0 action=error reward=0.00 done=true error={str(e)}", flush=True)
        success, score = False, 0.0
    finally:
        # 8. [END] LOG - Mandatory Format
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.3f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()