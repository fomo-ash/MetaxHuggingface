import random


class StudentLifeEnv:
    def __init__(self):
        self.max_steps = 168
        self.reset()

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

    def state(self):
        return self.state_data

    # =========================
    # 🧠 REASONING SYSTEM
    # =========================
    def generate_reason(self, action, subject, weakest):
        energy = self.state_data["energy"]
        stress = self.state_data["stress"]
        revision = self.state_data["revision_level"]

        if energy <= 0:
            return "Energy depleted → only rest is effective"

        if stress >= 1:
            return "Stress too high → recovery needed"

        if energy < 0.2:
            return "Low energy → inefficient learning"

        if stress > 0.8:
            return "High stress → reduced performance"

        if action == "study_new_topic":
            if subject == weakest:
                return f"Studying weakest subject ({subject})"
            return "Studying to improve overall mastery"

        elif action == "revise":
            if revision < 0.3:
                return "Low revision → strengthening memory"
            return "Maintaining retention"

        elif action == "mock_test":
            return "Testing preparation level"

        elif action == "rest":
            return "Recovering energy and reducing stress"

        elif action == "skip":
            return "No productive action taken"

        return "Unknown action handled safely"

    # =========================
    # 🚀 STEP FUNCTION
    # =========================
    def step(self, action):
        self.step_count += 1
        reward = 0

        # -------------------------
        # 🧠 INPUT NORMALIZATION
        # -------------------------
        if not isinstance(action, str):
            action = "skip"
        else:
            action = action.lower().strip()

        if any(k in action for k in ["study", "learn"]):
            action = "study_new_topic"
        elif any(k in action for k in ["revise", "review"]):
            action = "revise"
        elif any(k in action for k in ["test", "exam", "quiz"]):
            action = "mock_test"
        elif any(k in action for k in ["rest", "sleep", "break"]):
            action = "rest"
        elif any(k in action for k in ["skip", "idle"]):
            action = "skip"
        else:
            action = "unknown"

        # -------------------------
        # 🚨 CRITICAL STATE
        # -------------------------
        if self.state_data["energy"] <= 0 or self.state_data["stress"] >= 1:
            if action == "rest":
                self.state_data["energy"] += 0.3
                self.state_data["stress"] -= 0.2

                self.state_data["energy"] = min(1, self.state_data["energy"])
                self.state_data["stress"] = max(0, self.state_data["stress"])

                return self.state(), 0.2, False, {
                    "reason": "Critical state → recovery via rest",
                    "decision_quality": "good"
                }

            return self.state(), -1, False, {
                "reason": "Exhausted → only rest works",
                "decision_quality": "poor"
            }

        # -------------------------
        # 🎲 RANDOM EVENT
        # -------------------------
        if random.random() < 0.05:
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.1
            reward -= 0.2

        subjects = self.state_data["subjects"]

        # ✅ correct weakest BEFORE update
        weakest = min(subjects, key=subjects.get)

        # bias toward weakest
        subject = weakest if random.random() < 0.7 else random.choice(list(subjects.keys()))

        # -------------------------
        # 🎯 ACTIONS
        # -------------------------
        if action == "study_new_topic":
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.05

            progress = random.uniform(0.02, 0.05)

            if self.state_data["energy"] < 0.25:
                progress *= 0.5

            subjects[subject] += progress
            self.state_data["revision_level"] += 0.01

            reward += progress * 10

            if subject == weakest:
                reward += 0.3

        elif action == "revise":
            self.state_data["energy"] -= 0.08
            self.state_data["revision_level"] += 0.05
            reward += 0.6

        elif action == "mock_test":
            self.state_data["energy"] -= 0.1

            avg = sum(subjects.values()) / len(subjects)

            score = avg * 100
            score *= (1 - self.state_data["stress"] * 0.2)

            score += random.uniform(-5, 10)
            score = max(0, min(100, score))

            self.state_data["mock_test_score"] = score
            reward += score / 50

        elif action == "rest":
            self.state_data["energy"] += 0.2
            self.state_data["stress"] -= 0.1
            reward += 0.2

            if self.state_data["energy"] > 0.95:
                reward -= 0.2

        elif action == "skip":
            self.state_data["stress"] += 0.1
            reward -= 0.5

        else:
            reward -= 0.2
            self.state_data["stress"] += 0.05

        # -------------------------
        # 🔥 DECAY
        # -------------------------
        if action != "revise":
            self.state_data["revision_level"] *= 0.985

        avg = sum(subjects.values()) / len(subjects)

        self.state_data["forgetting_risk"] = max(
            0,
            min(1, 1 - (0.6 * self.state_data["revision_level"] + 0.4 * avg))
        )

        self.state_data["forgetting_risk"] += 0.005

        self.state_data["learning_efficiency"] = self.state_data["mock_test_score"] / 100

        self.state_data["confidence"] = (
            0.4 * self.state_data["revision_level"] +
            0.6 * avg
        )

        # -------------------------
        # 😈 REGRET
        # -------------------------
        if action in ["study_new_topic", "revise", "mock_test"]:
            effort = max(0, 1 - self.state_data["energy"])
            regret = effort - avg
            regret = max(-0.5, min(0.5, regret))
            reward -= regret * 0.05

        # -------------------------
        # ⚡ ENERGY SCALING
        # -------------------------
        reward *= max(0.2, self.state_data["energy"])

        # -------------------------
        # 🔒 CLAMP
        # -------------------------
        for sub in subjects:
            subjects[sub] = max(0, min(1, subjects[sub]))

        self.state_data["energy"] = max(0, min(1, self.state_data["energy"]))
        self.state_data["stress"] = max(0, min(1, self.state_data["stress"]))
        self.state_data["revision_level"] = max(0, min(1, self.state_data["revision_level"]))
        self.state_data["forgetting_risk"] = max(0, min(1, self.state_data["forgetting_risk"]))

        # -------------------------
        # ⏳ TIME
        # -------------------------
        if self.step_count % 24 == 0:
            self.state_data["exam_days_left"] -= 1

            if self.state_data["exam_days_left"] <= 2:
                self.state_data["stress"] += 0.05

        reward = max(-1, min(1, reward))

        done = self.step_count >= self.max_steps or self.state_data["exam_days_left"] <= 0

        # -------------------------
        # 🧠 FINAL OUTPUT
        # -------------------------
        reason = self.generate_reason(action, subject, weakest)

        # 🎯 DECISION QUALITY
        energy = self.state_data["energy"]
        stress = self.state_data["stress"]

        if reward > 0.2:
            decision_quality = "good"
        elif reward > 0:
            decision_quality = "neutral"
        else:
            decision_quality = "poor"

        # overrides
        if action == "rest" and energy < 0.3:
            decision_quality = "good"

        if action == "revise" and self.state_data["revision_level"] < 0.3:
            decision_quality = "good"

        if action == "study_new_topic" and energy < 0.2:
            decision_quality = "poor"

        if stress > 0.85 and action != "rest":
            decision_quality = "poor"

        return self.state(), reward, done, {
            "reason": reason,
            "decision_quality": decision_quality
        }