import random
import copy


class StudentLifeEnv:
    def __init__(self):
        self.max_steps = 168
        self.reset()

    # -------------------------
    # RESET
    # -------------------------
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

    # -------------------------
    # STATE
    # -------------------------
    def state(self):
        return copy.deepcopy(self.state_data)

    # -------------------------
    # STEP
    # -------------------------
    def step(self, action):
        self.step_count += 1
        reward = 0

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

        if action == "study_new_topic":
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.05
            progress = random.uniform(0.02, 0.05)
            subjects[subject] += progress
            reward += progress * 10

        elif action == "revise":
            self.state_data["energy"] -= 0.08
            self.state_data["revision_level"] += 0.05
            reward += 0.6

        elif action == "mock_test":
            self.state_data["energy"] -= 0.1
            avg = sum(subjects.values()) / len(subjects)
            score = avg * 100
            self.state_data["mock_test_score"] = score
            reward += score / 50

        elif action == "rest":
            self.state_data["energy"] += 0.2
            self.state_data["stress"] -= 0.1
            reward += 0.2

        elif action == "skip":
            self.state_data["stress"] += 0.1
            reward -= 0.5

        # clamp
        for sub in subjects:
            subjects[sub] = max(0, min(1, subjects[sub]))

        self.state_data["energy"] = max(0, min(1, self.state_data["energy"]))
        self.state_data["stress"] = max(0, min(1, self.state_data["stress"]))

        reward = max(-1, min(1, reward))

        done = self.step_count >= self.max_steps

        return self.state(), reward, done, {}

    # -------------------------
    # FINAL SCORE (FIXED)
    # -------------------------
    def final_score(self):
        subjects = self.state_data.get("subjects", {})

        if not subjects:
            return {"error": "no data"}

        avg = sum(subjects.values()) / len(subjects)

        energy = float(self.state_data.get("energy", 0))
        stress = float(self.state_data.get("stress", 0))
        revision = float(self.state_data.get("revision_level", 0))
        mock_score = float(self.state_data.get("mock_test_score", 0))
        confidence = float(self.state_data.get("confidence", 0))
        forgetting = float(self.state_data.get("forgetting_risk", 0))

        efficiency = avg * energy * (1 - stress)

        return {
            "scores": {
                "average_subject_mastery": avg,
                "revision_level": revision,
                "mock_test_score": mock_score / 100,
                "confidence": confidence,
                "efficiency_score": efficiency
            },
            "health": {
                "energy": energy,
                "stress": stress,
                "forgetting_risk": forgetting
            },
            "final_assessment": self._compute_final_grade(avg)
        }

    def _compute_final_grade(self, avg):
        if avg > 0.8:
            return "Excellent"
        elif avg > 0.6:
            return "Good"
        elif avg > 0.4:
            return "Average"
        else:
            return "Needs Improvement"