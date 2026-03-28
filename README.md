# 🎓 Engineering Exam Strategy Environment (OpenEnv)

A real-world reinforcement learning environment that simulates engineering exam preparation, where an AI agent must balance study, revision, testing, and well-being under time constraints.

---

## 🚀 Overview

This environment models the **decision-making process of a student preparing for competitive engineering exams** (e.g., JEE, GATE).

At each step, the agent chooses actions such as studying, revising, or taking mock tests, while managing:

- ⚡ Energy  
- 😰 Stress  
- 📘 Syllabus completion  
- 🔁 Revision level  
- 🧪 Mock test performance  
- ⏳ Time until exam  

The goal is to learn **optimal strategies under realistic trade-offs**.

---

## 🧠 Key Features

- ✅ Real-world scenario (exam preparation)
- ✅ Multi-objective optimization (performance vs well-being)
- ✅ Continuous reward shaping
- ✅ Partial progress tracking (non-binary scoring)
- ✅ Stochastic events (random disruptions)
- ✅ Robust API (handles noisy inputs)

---

## 🎮 Action Space

| Action | Description |
|------|-------------|
| `study_new_topic` | Learn new concepts (increases syllabus completion) |
| `revise` | Reinforce knowledge (improves retention) |
| `mock_test` | Evaluate performance |
| `rest` | Recover energy, reduce stress |
| `skip` | Do nothing (penalty) |

---

## 📊 Observation Space

```json
{
  "energy": float (0–1),
  "stress": float (0–1),
  "syllabus_completion": float (0–1),
  "revision_level": float (0–1),
  "mock_test_score": float (0–100),
  "exam_days_left": int
}
