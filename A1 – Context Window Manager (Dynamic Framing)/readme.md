# A1 – Context Window Manager (Dynamic Framing)
_Attention & Context Controllers → Foundation Tier_

A1 builds a **Context Window Manager**: a system component that maintains multiple “frames” of context (task, social, temporal, risk, tools) and decides what should be **foreground** vs **background** at any moment.

If memory answers **what we know**, A1 answers:

- **What should we keep in the working set right now?**
- **What should be dropped, compressed, or parked?**
- **Which frame should dominate the agent’s thinking?**

This is the first step toward agents that don’t just “stuff the prompt”, but **actively manage attention**.

---

## What A1 Does

### Core capabilities
- Maintains multiple context frames:
  - **TASK**: goals, constraints, success criteria
  - **STATE**: current environment state summary
  - **SOCIAL**: stakeholders, roles, tone, commitments
  - **TEMPORAL**: deadlines, sequence, what just happened
  - **RISK**: safety, policy constraints, escalation triggers
  - **TOOLS**: tool availability, tool results, tool instructions
- Dynamically chooses a **foreground frame** based on signals
- Produces a **bounded context window** for the next reasoning step:
  - Promotes critical items into the window
  - Compresses older items
  - Drops low-value items

---

## Why This Matters

Most agent failures are not because the model is “dumb”.
They happen because the agent’s working context is:
- noisy
- stale
- misframed
- dominated by irrelevant details

A1 makes framing explicit.

---

## Inputs and Outputs

### Inputs
- Events (messages, observations, tool results)
- Task metadata (goal, constraints, preferences)
- Attention signals (urgency, risk flags, novelty, role)

### Output
A single structured object:

- `foreground_frame`: which frame dominates right now
- `context_window`: the actual bounded context text for the model
- `frame_state`: internal state snapshot (debuggable)

---

## Minimal API

- `update(event)`  
  Ingests a new event and updates frames.

- `set_goal(goal, constraints=None)`  
  Initializes task frame.

- `choose_foreground()`  
  Selects which frame should be dominant.

- `render_context(budget_chars=2000)`  
  Generates the bounded context window.

---

## Demo Scenario Included

A small runnable demo simulates:
- setting a goal
- receiving messages
- receiving tool outputs
- encountering a risk flag
- switching foreground frames dynamically

Run:
- `python a1_context_window_manager.py`

---

## Next Steps

After A1, we will build:
- A2 (Attention Budgeting Engine): hard compute budgets
- A3 (Salience-Driven Memory Access): selective memory recall gated by A1
