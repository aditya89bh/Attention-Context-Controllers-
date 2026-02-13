# A6 — Goal Arbitration & Conflict Resolution Controller
_Strategic dominance resolution for multi-threaded agents (no ML training)._

A6 decides **which goal should run right now** when multiple goals/tasks exist (especially after A5 introduces interruption + task switching). It introduces **priority scoring, utility arbitration, conflict detection, and preemption rules**.

This project is:
- **Pure Python**
- **Modular**
- **Colab-runnable**
- **Independent but layered** (plugs into A1–A5 conceptually)
- **Focused on agent behavior** (system design, not LLM internals)

---

## Why A6 Exists (and Why It Follows A5)

A5 enables:
- multiple active threads
- interruptions
- task switching

But A5 alone is reactive. It answers: _“Can I switch?”_  
A6 answers: _“Should I switch, and to what?”_

Without A6:
- Interrupts can hijack execution.
- No global prioritization.
- Threads compete with no dominance logic.

---

## Cognitive Control Primitive

**Strategic dominance resolution**  
A6 computes a dominance decision using:
- goal priority
- expected utility / urgency
- conflicts between goals
- preemption rules and cooldowns

Output is a **Run Directive**:
- continue current goal
- preempt and switch to another goal
- pause or defer a goal
- reject a goal (hard conflict / policy block)

---

## Inputs and Outputs

### Inputs (from layered system)
A6 is designed to consume signals from earlier layers:

- From **A1 Context Framing**:
  - current context tags (e.g., `work`, `safety`, `deadline`)
  - situational constraints (soft)

- From **A2 Attention Budgeting**:
  - available attention/time budget
  - cognitive load estimate

- From **A3 Salience-Driven Memory Access**:
  - recalled goal-related evidence (past outcomes, penalties)
  - recent failures or success priors

- From **A4 Temporal Context**:
  - timestamps, deadlines, time-since-last-progress
  - urgency and decay functions

- From **A5 Task Switching**:
  - active threads
  - interruption events
  - task switching cost estimates

### Outputs
- `selected_goal_id`
- `directive` (CONTINUE | SWITCH | PAUSE | DEFER | REJECT)
- `why` (structured rationale: scores + conflicts + applied rules)

---

## Core Concepts

### 1) Goal Representation
Each goal is defined with:
- `priority` (baseline importance)
- `urgency` (time pressure, deadlines)
- `utility` (expected value if pursued now)
- `cost` (estimated resource consumption)
- `switch_cost` (from A5)
- `risk` (optional; can be used later by A11 if you ever add it)
- `constraints` (tags it must respect; A7 will formalize this)

### 2) Arbitration Score
A6 computes a **dominance score**:

**Score(goal) = wP*Priority + wU*Utility + wT*Urgency - wC*Cost - wS*SwitchCost - ConflictPenalty**

Weights are configurable. Keep them simple and deterministic.

### 3) Conflict Detection
Goals can conflict by:
- shared exclusive resources (only one can run)
- mutually exclusive states
- contradictory commitments

A6 detects conflicts via:
- goal tags (e.g., `requires:focus`, `requires:network`, `exclusive:gpu`)
- explicit conflict rules
- runtime conflicts (active goal holding a lock)

### 4) Preemption Rules
Preemption defines when a new goal can interrupt the current one.

Example policies:
- **Hard preempt**: safety or deadline-critical goals always preempt
- **Soft preempt**: only preempt if score exceeds current by threshold
- **Cooldown**: do not switch too frequently (anti-thrashing)
- **Commitment window**: minimum time slice before switching

---

## Project Structure (Suggested)

