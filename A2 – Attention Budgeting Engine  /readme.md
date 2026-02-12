# A2 – Attention Budgeting Engine  
_Attention & Context Controllers → Foundation Tier_

A2 introduces **bounded cognition** to AI agents.

If A1 decides:

> What should we focus on?

A2 decides:

> How much thinking are we allowed to spend?

This project implements a finite **Attention Budget** that governs reasoning depth, memory access, tool usage, and planning steps. Instead of assuming infinite compute, agents operate under constrained cognitive resources.

---

## Why This Exists

Most agent systems:
- Overthink simple tasks
- Call too many tools
- Retrieve excessive memory
- Loop indefinitely
- Collapse under overload

Real intelligence is resource-bounded.

Humans:
- Prioritize under time pressure
- Switch to heuristics when tired
- Reduce depth when resources are low

A2 models this constraint explicitly.

---

## Core Concept

Each episode is allocated a fixed attention budget.

Budget can represent:
- Planning steps
- Memory retrieval operations
- Tool calls
- Context rendering operations
- Cognitive cost units

Every operation deducts from the total budget.

When budget depletes:
- Context shrinks
- Memory recall is limited
- Planning depth reduces
- Heuristic mode activates
- Execution may terminate early

---

## Budget Modes

Based on remaining units, the system operates in one of three modes:

- **FULL**  
  Deep reasoning allowed. Full context access.

- **CONSERVATIVE**  
  Limited retrieval. Reduced planning depth.

- **CRITICAL**  
  Minimal reasoning. Heuristic shortcuts. Emergency completion behavior.

This enables graceful degradation instead of system collapse.

---

## Core Components

### AttentionBudget
Tracks:
- Total units
- Remaining units
- Depletion ratio
- Current budget mode

### Cost Model
Defines cognitive costs for:
- Memory access
- Tool usage
- Planning steps
- Context rendering

### Budget Controller
- Deducts cost per operation
- Enforces mode transitions
- Signals behavioral constraints to agent layers

---

## Relationship to A1

A1:
> What should we think about?

A2:
> How deeply are we allowed to think?

Together they form the beginning of a cognitive control stack:

Perception  
→ Attention (A1)  
→ Effort Allocation (A2)  
→ Memory Access  
→ Policy  
→ Action  

---

## Demo Scenario

The included demo simulates:
- Initializing a fixed attention budget
- Performing reasoning steps
- Making tool calls
- Retrieving memory
- Observing budget depletion
- Automatic transition between FULL → CONSERVATIVE → CRITICAL modes

Run:

```bash
python demo.py
