---
title: Adaptive Exam RL
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---


# 🎓 Adaptive Engineering Exam Strategy Environment (OpenEnv)

A **multi-factor reinforcement learning environment** that simulates real-world engineering exam preparation.
An AI agent must learn **optimal study strategies** under constraints of time, energy, stress, and memory decay.

---

## 🌐 Live API

👉 https://fomo-ash-adaptive-exam-rl.hf.space/docs

---

## 🚀 Overview

Preparing for competitive engineering exams (e.g., JEE, GATE) is not just about studying more — it is about **studying smart**.

At each timestep, an agent must decide:

* 📚 Study new topics
* 🔁 Revise to retain knowledge
* 🧪 Take mock tests
* 😴 Rest to recover

All while managing:

* ⚡ Energy (fatigue)
* 😰 Stress (cognitive load)
* 🧠 Memory & forgetting
* 📊 Subject-wise mastery
* ⏳ Time until exam

---

## 🧠 Core Idea

> A strategic decision-making system balancing:

```
Learning Gain  vs  Retention
Performance    vs  Fatigue
Short-term Gain vs Long-term Efficiency
```

---

## 🎯 Objective

Maximize exam readiness by:

* Completing syllabus across subjects
* Maintaining strong retention
* Achieving high mock test scores
* Managing energy and stress efficiently

---

## 🎮 Action Space

| Action          | Description                             |
| --------------- | --------------------------------------- |
| study_new_topic | Learn new concepts (improves mastery)   |
| revise          | Strengthens memory & reduces forgetting |
| mock_test       | Evaluates performance                   |
| rest            | Recovers energy, reduces stress         |
| skip            | No productive action (penalty)          |

### 🧠 Flexible Inputs

```
"study", "learn" → study_new_topic  
"test", "exam" → mock_test  
"sleep", "rest" → rest  
```

---

## 📊 Observation Space

```json
{
  "energy": 0-1,
  "stress": 0-1,
  "subjects": {
    "math": 0-1,
    "physics": 0-1,
    "chemistry": 0-1
  },
  "revision_level": 0-1,
  "mock_test_score": 0-100,
  "confidence": 0-1,
  "forgetting_risk": 0-1,
  "learning_efficiency": 0-1,
  "exam_days_left": int
}
```

---

## 🔁 Environment Dynamics

Each step:

```
Action → State Update → Reward → Progress
```

Includes:

* 🎲 Random disruptions
* 📉 Knowledge decay
* ⚖️ Trade-offs between actions
* 🔁 Continuous learning evolution

---

## 😈 Reward Function

```
Reward =
+ Learning Gain
+ Weak Subject Bonus
+ Performance Gain
- Effort Cost
- Stress Penalty
- Regret (inefficient actions)
```

---

## 🧪 Evaluation System

| Task   | Description                   |
| ------ | ----------------------------- |
| Easy   | Maximize subject completion   |
| Medium | Balance completion + revision |
| Hard   | Optimize full exam readiness  |

All graders return scores in **[0.0 – 1.0]**

---

## 🤖 Baseline Agent

Run:

```bash
python inference.py
```

Features:

* Focuses on weakest subject
* Maintains revision
* Manages energy & stress
* Takes tests strategically

---

## 🐳 Run Locally

### FastAPI

```bash
uvicorn main:app --reload
```

### Docker

```bash
docker build -t exam-env .
docker run -p 7860:7860 exam-env
```

---

## 🔌 API Endpoints

| Endpoint         | Description       |
| ---------------- | ----------------- |
| GET /reset       | Reset environment |
| POST /step       | Take action       |
| GET /state       | Current state     |
| GET /final_score | Final performance |
| GET /tasks       | Task definitions  |

---

## 📦 OpenEnv Compliance

This environment follows OpenEnv standard:

* ✔ step()
* ✔ reset()
* ✔ state()
* ✔ openenv.yaml
* ✔ multi-task graders

---

## 🧠 Why This Matters

Models:

* Human learning behavior
* Cognitive constraints
* Strategic decision-making

---

## 🔥 Key Features

* Multi-dimensional state space
* Subject-wise learning tracking
* Forgetting + revision system
* Regret-based reward shaping
* Real-world constraints simulation

---

## 🚀 Future Work

* Knowledge graph dependencies
* Personalized learning agents
* LLM-based tutoring
* Multi-agent competition

---

## ✅ Submission Checklist

* ✔ OpenEnv API implemented
* ✔ Docker deployment working
* ✔ Hugging Face Space live
* ✔ inference.py included
* ✔ 3 graders implemented
* ✔ evaluation scripts added

---

## 🏁 Built With

* Python
* FastAPI
* OpenEnv Framework

---

💡 *Designed to simulate real-world learning — not just maximize scores.*
