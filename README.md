# Attention & Context Controllers  
_From Memory Systems to Cognitive Control_

This project explores **Attention and Context Controllers** for AI agents.

If memory answers:

> What does the system know?

Then attention answers:

> What matters right now?

And context answers:

> Why does it matter?

Most AI agents today:
- Retrieve too much
- Reason without prioritization
- Treat all signals equally
- Fail under overload
- Drift off-task

This repository builds a **control layer above memory**, enabling agents to:
- Dynamically focus
- Allocate cognitive budget
- Shift temporal modes
- Detect drift
- Respond to interruption
- Modulate reasoning depth

This is not about bigger models.  
This is about better control.

---

## Why This Project Exists

Modern agent stacks often include:
- Tool use
- Memory retrieval
- Planning loops
- Multi-agent communication

But they lack an explicit **attention system**.

Without attention:
- Memory becomes noise
- Planning becomes expensive
- Multi-agent coordination becomes chaotic
- Long-horizon tasks degrade

Attention is the gatekeeper of cognition.

This repository implements it explicitly.

---

## Core Architecture

```
Perception
→ Attention
→ Memory Access
→ Context Framing
→ Policy
→ Action

```


### Attention Layer Responsibilities

- Select relevant inputs
- Score memory salience
- Allocate reasoning budget
- Control temporal mode
- Detect drift
- Handle interrupts
- Route to appropriate policy depth

Attention is treated as a **first-class system component**, not a side effect of prompting.

---

## Project Structure

### Foundation Tier

#### A1 – Context Window Manager
Dynamic framing of task, social, and temporal context.

#### A2 – Attention Budgeting Engine
Finite cognitive budget allocation across reasoning steps.

#### A3 – Salience-Driven Memory Access
Selective memory retrieval based on task-conditioned scoring.

#### A4 – Temporal Context Controller
Explicit separation of past recall, present execution, and simulation.

#### A5 – Interrupt & Override Controller
Priority-based preemption of ongoing cognition.

---

### Advanced Tier

#### A6 – Meta-Attention
Monitoring and correcting attention allocation patterns.

#### A7 – Role-Conditioned Attention
Different attention filters for different agent roles.

#### A8 – Social Attention Controller
Attention allocation across multi-agent dialogue.

#### A9 – Context Drift Detection
Long-horizon task alignment monitoring.

#### A10 – Context → Policy Router
Dynamic routing between shallow heuristics and deep planning.

---

## Design Principles

1. Attention is scarce.
2. Context is dynamic.
3. Memory must be filtered.
4. Cognition must degrade gracefully.
5. Interruptions must be first-class events.
6. Multi-agent systems require attention governance.

---

## What This Is Not

- Not prompt engineering tricks
- Not just RAG tuning
- Not fine-tuning a model
- Not larger context windows

This is a systems layer.

---

## Relationship to Memory Projects

This repository builds on:

- Shared Memory Systems
- Multi-Agent Salience
- Organizational Memory
- Theory of Mind Memory

Memory stores.  
Attention selects.  
Context frames.  
Policy acts.

Together they form a cognitive loop.

---

## Future Extensions

- Attention-conditioned world models
- Energy-based cognition models
- Hierarchical attention stacks
- Embodied attention for physical robots
- Cognitive load simulation for multi-agent teams

---

## Vision

The goal is to build agents that:
- Focus
- Adapt
- Prioritize
- Recover from overload
- Sustain coherence over time

In short:

Agents that don’t just think.  
Agents that know what to think about.

