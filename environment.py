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

            "syllabus_completion": 0.1,
            "revision_level": 0.0,
            "mock_test_score": 40,

            # Intelligence signals
            "confidence": 0.5,
            "forgetting_risk": 0.3,
            "learning_efficiency": 0.5,

            "exam_days_left": 7
        }

        return self.state()

    def state(self):
        return self.state_data

    def step(self, action):
        self.step_count += 1
        reward = 0

        # Normalize input
        action = action.lower().strip()

        if action in ["study", "learn"]:
            action = "study_new_topic"
        elif action in ["revise", "review"]:
            action = "revise"
        elif action in ["test", "exam"]:
            action = "mock_test"
        elif action in ["rest", "sleep", "break"]:
            action = "rest"
        elif action in ["skip", "idle"]:
            action = "skip"

        # Random event
        if random.random() < 0.05:
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.1
            reward -= 0.2

        # ACTIONS
        if action == "study_new_topic":
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.05

            progress = random.uniform(0.02, 0.05)
            self.state_data["syllabus_completion"] += progress
            reward += progress * 10

            if self.state_data["energy"] < 0.3:
                reward -= 0.5

        elif action == "revise":
            self.state_data["energy"] -= 0.08
            self.state_data["revision_level"] += 0.03
            reward += 0.5

        elif action == "mock_test":
            self.state_data["energy"] -= 0.1

            noise = random.uniform(-5, 10)
            base = self.state_data["syllabus_completion"] * 100
            revision_bonus = self.state_data["revision_level"] * 50

            score = base * 0.6 + revision_bonus * 0.4 + noise
            score = max(0, min(100, score))

            self.state_data["mock_test_score"] = score
            reward += score / 50

        elif action == "rest":
            self.state_data["energy"] += 0.2
            self.state_data["stress"] -= 0.1
            reward += 0.2  # keep rest positive

        elif action == "skip":
            self.state_data["stress"] += 0.1
            reward -= 0.5

        else:
            reward -= 0.2

        # Knowledge decay
        if action != "revise":
            self.state_data["revision_level"] *= 0.98

        # Update signals
        self.state_data["forgetting_risk"] = 1 - self.state_data["revision_level"]
        self.state_data["learning_efficiency"] = self.state_data["mock_test_score"] / 100
        self.state_data["confidence"] = (
            0.5 * self.state_data["revision_level"] +
            0.5 * (self.state_data["mock_test_score"] / 100)
        )

        # Regret (SAFE VERSION)
        if action in ["study_new_topic", "revise", "mock_test"]:
            effort = max(0, 1 - self.state_data["energy"])
            gain = self.state_data["syllabus_completion"]

            regret = effort - gain
            regret = max(-0.5, min(0.5, regret))  # clamp

            reward -= regret * 0.05

        # Penalties
        if self.state_data["energy"] <= 0:
            reward -= 1

        if self.state_data["stress"] >= 1:
            reward -= 1

        # Clamp state
        self.state_data["energy"] = max(0, min(1, self.state_data["energy"]))
        self.state_data["stress"] = max(0, min(1, self.state_data["stress"]))
        self.state_data["syllabus_completion"] = min(1.0, self.state_data["syllabus_completion"])
        self.state_data["revision_level"] = max(0, min(1, self.state_data["revision_level"]))

        # Time
        if self.step_count % 24 == 0:
            self.state_data["exam_days_left"] -= 1

            if self.state_data["exam_days_left"] <= 2:
                self.state_data["stress"] += 0.05

        # Clamp final reward (VERY IMPORTANT)
        reward = max(-1, min(1, reward))

        done = self.step_count >= self.max_steps or self.state_data["exam_days_left"] <= 0

        return self.state(), reward, done, {}