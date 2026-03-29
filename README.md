# 🎓 Adaptive Engineering Exam Strategy Environment (OpenEnv)

A **multi-factor reinforcement learning environment** that simulates real-world engineering exam preparation.
An AI agent must learn **optimal study strategies** under constraints of time, energy, stress, and memory decay.

---

## 🚀 Overview

Preparing for competitive engineering exams (e.g., JEE, GATE) is not just about studying more — it is about **studying smart**.

This environment models that reality.

At each timestep, an agent must decide:

* 📚 Should I study new topics?
* 🔁 Should I revise to retain knowledge?
* 🧪 Should I test my understanding?
* 😴 Should I rest to recover?

All while managing:

* ⚡ Energy (fatigue)
* 😰 Stress (cognitive load)
* 🧠 Memory & forgetting
* 📊 Subject-wise mastery
* ⏳ Time until exam

---

## 🧠 Core Idea

> This is not a simple simulator, it is a **decision-making system with trade-offs**.

The agent must balance:

```text
Learning Gain  vs  Retention
Performance    vs  Fatigue
Short-term Gain vs Long-term Efficiency
```

---

## 🎯 Objective

Maximize overall performance by:

* Completing syllabus across subjects
* Maintaining high retention (low forgetting)
* Achieving strong mock test scores
* Managing energy and stress effectively

---

## 🧩 Environment Design

### 📚 Subject-wise Learning

Instead of a single progress metric, learning is tracked per subject:

```json
{
  "subjects": {
    "math": 0.3,
    "physics": 0.3,
    "chemistry": 0.3
  }
}
```

* Learning is **stochastic**
* Weak subjects are prioritized
* Diminishing returns apply

---

### 🔁 Memory & Forgetting Model

* `revision_level` represents retention strength
* `forgetting_risk` increases when revision is low
* Knowledge decays over time

```text
No revision → memory decay → performance drop
```

---

### ⚡ Energy & Stress System

* Energy decreases with effort (study/test)
* Stress increases with workload
* Low energy reduces learning efficiency
* High stress reduces performance

---

### 🧪 Performance Modeling

Mock test scores depend on:

```text
Subject Mastery + Revision + Stress + Randomness
```

This ensures:

* No deterministic outcomes
* Realistic variability

---

### 😈 Regret-Based Reward System

The reward function models **efficiency of decisions**:

```text
Reward =
+ Learning Gain
+ Weak Topic Bonus
+ Performance Gain
- Effort Cost
- Stress / Burnout Penalty
- Inefficient Actions (Regret)
```

---

## 🎮 Action Space

| Action            | Description                                   |
| ----------------- | --------------------------------------------- |
| `study_new_topic` | Learn new concepts (improves subject mastery) |
| `revise`          | Strengthens memory & reduces forgetting       |
| `mock_test`       | Evaluates performance                         |
| `rest`            | Recovers energy, reduces stress               |
| `skip`            | No productive action (penalty)                |

### 🧠 Robust Input Handling

The environment supports flexible inputs:

```text
"study", "learn" → study_new_topic  
"exam", "test" → mock_test  
"sleep", "break" → rest  
Unknown input → safe penalty (no crash)
```

---

## 📊 Observation Space

```json
{
  "energy": float (0–1),
  "stress": float (0–1),
  "subjects": {
    "math": float (0–1),
    "physics": float (0–1),
    "chemistry": float (0–1)
  },
  "revision_level": float (0–1),
  "mock_test_score": float (0–100),
  "confidence": float (0–1),
  "forgetting_risk": float (0–1),
  "learning_efficiency": float (0–1),
  "exam_days_left": int
}
```

---

## 🔄 Environment Dynamics

Each step follows:

```text
Action → State Update → Metric Update → Reward Calculation
```

### Includes:

* 🎲 Random life events (unexpected disruptions)
* 📉 Knowledge decay over time
* ⚖️ Trade-offs between actions
* 🔁 Continuous state evolution

---

## 🧪 Evaluation System

The environment is evaluated using **multi-level graders**:

### ✅ Easy

* Basic progress (subjects, completion)

### ⚙️ Medium

* Balanced strategy (energy, stress, revision)

### 🔥 Hard

* Overall reward efficiency & long-term performance

---

## 🐳 Deployment & API

### Run locally:

```bash
uvicorn main:app --reload
```

### Endpoints:

* `GET /reset` → Reset environment
* `POST /step?action=...` → Take action
* `GET /state` → Current state

---

## 🤖 Baseline Agent

A rule-based agent is included:

* Studies weak topics
* Revises when needed
* Takes tests strategically
* Manages energy

Benchmark results show:

* ✔ Significant improvement over random agent
* ✔ Stable multi-metric performance

---

## 🧠 Why This Matters

This project models:

* Human learning behavior
* Cognitive limitations
* Strategic planning under constraints

---

## 🔥 What Makes It Unique

* Multi-dimensional state space
* Realistic learning + forgetting dynamics
* Regret-based reward shaping
* Robust to noisy inputs
* Designed for RL benchmarking

---

## 🚀 Future Extensions

* Knowledge graph for prerequisites
* Personalized learning styles
* LLM-driven tutoring integration
* Multi-agent competition

---

## 📌 Summary

> This environment transforms exam preparation into a **strategic decision-making problem**, enabling AI agents to learn **how to learn efficiently**.

---

## 🏁 Built With

* Python
* FastAPI
* OpenEnv Framework

---

## 📬 Submission

Includes:

* ✅ OpenEnv-compatible API
* ✅ Docker container
* ✅ Automated graders
* ✅ Evaluation scripts

---

💡 *Designed to simulate real-world learning — not just optimize scores.*
