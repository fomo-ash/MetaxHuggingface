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

            # 🔥 SUBJECTS (NEW CORE)
            "subjects": {
                "math": 0.3,
                "physics": 0.3,
                "chemistry": 0.3
            },

            "revision_level": 0.0,
            "mock_test_score": 40,

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

        action = action.lower().strip()

        if "study" in action:
            action = "study_new_topic"
        elif "revise" in action or "review" in action:
            action = "revise"
        elif "test" in action or "exam" in action:
            action = "mock_test"
        elif "rest" in action or "sleep" in action:
            action = "rest"
        elif "skip" in action:
            action = "skip"

        # random event
        if random.random() < 0.05:
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.1
            reward -= 0.2

        # pick subject
        subject = random.choice(list(self.state_data["subjects"].keys()))
        weakest = min(self.state_data["subjects"], key=self.state_data["subjects"].get)

        # ACTIONS
        if action == "study_new_topic":
            self.state_data["energy"] -= 0.1
            self.state_data["stress"] += 0.05

            progress = random.uniform(0.02, 0.05)

            if self.state_data["energy"] < 0.2:
                progress *= 0.5  # burnout

            self.state_data["subjects"][subject] += progress

            reward += progress * 10

            if subject == weakest:
                reward += 0.2

        elif action == "revise":
            self.state_data["energy"] -= 0.08
            self.state_data["revision_level"] += 0.03
            reward += 0.5

        elif action == "mock_test":
            self.state_data["energy"] -= 0.1

            avg = sum(self.state_data["subjects"].values()) / 3
            score = avg * 100 + random.uniform(-5, 10)
            score = max(0, min(100, score))

            self.state_data["mock_test_score"] = score
            reward += score / 50

        elif action == "rest":
            self.state_data["energy"] += 0.2
            self.state_data["stress"] -= 0.1
            reward += 0.2

        elif action == "skip":
            self.state_data["stress"] += 0.1
            reward -= 0.5

        else:
            reward -= 0.2

        # decay
        if action != "revise":
            self.state_data["revision_level"] *= 0.98

        avg = sum(self.state_data["subjects"].values()) / 3

        self.state_data["forgetting_risk"] = 1 - self.state_data["revision_level"]
        self.state_data["learning_efficiency"] = self.state_data["mock_test_score"] / 100
        self.state_data["confidence"] = 0.5 * self.state_data["revision_level"] + 0.5 * avg

        # regret
        if action in ["study_new_topic", "revise", "mock_test"]:
            effort = max(0, 1 - self.state_data["energy"])
            regret = effort - avg
            regret = max(-0.5, min(0.5, regret))
            reward -= regret * 0.05

        # penalties
        if self.state_data["energy"] <= 0:
            reward -= 1
        if self.state_data["stress"] >= 1:
            reward -= 1

        # clamp
        for sub in self.state_data["subjects"]:
            self.state_data["subjects"][sub] = min(1.0, self.state_data["subjects"][sub])

        self.state_data["energy"] = max(0, min(1, self.state_data["energy"]))
        self.state_data["stress"] = max(0, min(1, self.state_data["stress"]))
        self.state_data["revision_level"] = max(0, min(1, self.state_data["revision_level"]))

        # time
        if self.step_count % 24 == 0:
            self.state_data["exam_days_left"] -= 1

        reward = max(-1, min(1, reward))

        done = self.step_count >= self.max_steps or self.state_data["exam_days_left"] <= 0

        return self.state(), reward, done, {}