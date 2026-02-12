# A3 – Salience-Driven Memory Access
_Attention & Context Controllers → Foundation Tier_

A3 introduces selective memory retrieval for AI agents.

If A1 decides:
> What context frame dominates?

And A2 decides:
> How much cognitive effort is available?

Then A3 decides:

> Which memories are important enough to enter reasoning?

Instead of retrieving memory blindly, A3 applies salience scoring to dynamically filter and rank memory candidates before they enter the agent’s working context.

---

## Why This Exists

Most memory systems:
- Retrieve top-k via embedding similarity
- Ignore task relevance shifts
- Ignore risk and urgency
- Overload context windows
- Create reasoning noise

Similarity ≠ importance.

Salience is dynamic.
It depends on:
- Current task
- Temporal urgency
- Risk level
- Agent role
- Budget mode (A2)

A3 makes memory gating explicit.

---

## Core Concept

Each memory item has:

- Base relevance (similarity or tag match)
- Recency
- Risk weight
- Task alignment score
- Context frame compatibility

These signals combine into a:

Salience Score

Only the top-ranked memories within a bounded limit are allowed into the reasoning window.

---

## Memory Selection Pipeline

1. Retrieve candidate memories (vector search or metadata match)
2. Compute salience score per memory
3. Adjust scores based on:
   - Foreground frame (A1)
   - Budget mode (A2)
4. Select top-k
5. Pass filtered memories into reasoning

---

## Core Components

### MemoryItem
Represents a stored memory with:
- Content
- Metadata
- Timestamp
- Base relevance
- Tags

### SalienceScorer
Computes weighted salience scores based on:
- Task relevance
- Recency decay
- Risk boost
- Frame alignment

### MemoryGate
Applies:
- Budget constraints (A2)
- Frame conditioning (A1)
- Top-k filtering

---

## Relationship to Previous Projects

A1:
> What frame dominates?

A2:
> How deeply are we allowed to think?

A3:
> Which memories are allowed to influence reasoning?

Together:

Perception  
→ Attention Framing (A1)  
→ Effort Allocation (A2)  
→ Memory Gating (A3)  
→ Policy  
→ Action  

---

## Demo Scenario

The demo simulates:
- A memory store with mixed relevance
- Task change
- Risk spike
- Budget reduction
- Dynamic shift in which memories are selected

Run:

```bash
python demo.py
