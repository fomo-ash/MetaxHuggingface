import random
import copy
from tasks import TASKS


class StudentLifeEnv:
    def __init__(self):
        self.max_steps = 168
        self.tasks = TASKS
        self.reset()

    # -------- TASK ACCESS (REQUIRED BY VALIDATOR) --------
    def get_tasks(self):
        return self.tasks

    # -------- RESET --------
    def reset(self):
        self.step_count = 0
        self.state_data = {
            "energy": 1.0,
            "stress": 0.2,
            "subjects": {
                "math": 0.3,
                "physics": 0.3,
                "chemistry": 0.3
            },
            "revision_level": 0.1,
            "mock_test_score": 40,
            "confidence": 0.4,
            "forgetting_risk": 0.5,
            "learning_efficiency": 0.4,
            "exam_days_left": 7
        }
        return self.state()

    # -------- STATE --------
    def state(self):
        return copy.deepcopy(self.state_data)

    # -------- STEP --------
    def step(self, action):
        self.step_count += 1
        reward = 0

        # Normalize action
        if not isinstance(action, str):
            action = "skip"
        else:
            action = action.lower().strip()

        if "study" in action:
            action = "study_new_topic"
        elif "revise" in action or "review" in action:
            action = "revise"
        elif "test" in action:
            action = "mock_test"
        elif "rest" in action:
            action = "rest"
        else:
            action = "skip"

        subjects = self.state_data["subjects"]
        weakest = min(subjects, key=subjects.get)
        subject = weakest if random.random() < 0.7 else random.choice(list(subjects.keys()))

        # ---- ACTION LOGIC ----
        if action == "study_new_topic":
            if self.state_data["energy"] > 0:
                self.state_data["energy"] -= 0.1
                self.state_data["stress"] += 0.05
                progress = random.uniform(0.02, 0.05)
                subjects[subject] += progress
                reward += progress * 10
            else:
                self.state_data["stress"] += 0.15
                reward -= 0.5

        elif action == "revise":
            if self.state_data["energy"] > 0:
                self.state_data["energy"] -= 0.08
                self.state_data["revision_level"] += 0.05
                reward += 0.6
            else:
                self.state_data["stress"] += 0.1
                reward -= 0.3

        elif action == "mock_test":
            energy_multiplier = 1.0 if self.state_data["energy"] > 0.2 else 0.5
            self.state_data["energy"] -= 0.1
            avg = sum(subjects.values()) / len(subjects)
            score = (avg * 100) * energy_multiplier
            self.state_data["mock_test_score"] = score
            reward += score / 50

        elif action == "rest":
            self.state_data["energy"] += 0.2
            self.state_data["stress"] -= 0.1
            reward += 0.2

        elif action == "skip":
            self.state_data["stress"] += 0.1
            reward -= 0.5

        # ---- CLAMP VALUES ----
        for sub in subjects:
            subjects[sub] = max(0, min(1, subjects[sub]))

        self.state_data["energy"] = max(0, min(1, self.state_data["energy"]))
        self.state_data["stress"] = max(0, min(1, self.state_data["stress"]))

        reward = max(-1, min(1, reward))
        done = self.step_count >= self.max_steps

        return self.state(), reward, done, {}

    # -------- FINAL SCORE (CRITICAL FIX) --------
    def final_score(self):
        """
        MUST return task → score mapping
        Validator uses this to count tasks + graders
        """
        return {
            task["name"]: task["grader"](self, 0)
            for task in self.tasks
        }