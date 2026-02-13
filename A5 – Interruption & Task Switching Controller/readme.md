# A5 – Interruption & Task Switching Controller
_Attention & Context Controllers → Foundation Tier_

A5 introduces controlled interruption handling for AI agents.

Most agents collapse under interruptions:
- They lose the original goal
- They merge unrelated threads
- They forget what they were doing
- They restart from scratch
- They drift into the latest message

A5 fixes this by making task switching explicit.

---

## Why This Exists

Real environments are interrupt-driven:
- Users change requirements mid-flow
- Tools return results asynchronously
- Safety/risk flags appear late
- Multiple tasks compete for attention

Without a controller, the agent becomes:
- reactive
- incoherent
- context-bloated
- unable to resume work cleanly

A5 makes interruption a first-class system behavior.

---

## Core Concept

The agent maintains a set of **active threads**:

- Current task thread (foreground)
- Paused threads (background)
- Interrupt thread (temporary foreground)
- Completed threads (archived)

Each thread stores:
- its goal
- its current step
- a minimal resume context
- pending actions
- last known state

---

## Thread Lifecycle

1. START thread (new task)
2. PAUSE thread (save resume snapshot)
3. INTERRUPT (spawn or attach)
4. RESUME (restore snapshot + continue)
5. MERGE (optional: combine related threads)
6. ARCHIVE (done)

---

## Interruption Policies

A5 classifies incoming events:
- Minor: append to current thread
- Blocking: pause current thread, handle interrupt
- Critical: override everything (e.g., risk/safety)
- Deferrable: queue for later

---

## Relationship to Previous Projects

A1: chooses the dominant context frame  
A2: allocates cognitive budget  
A3: gates which memories enter reasoning  
A4: enforces temporal mode isolation  
A5: manages multi-threaded attention over time

Together:

Perception  
→ Framing (A1)  
→ Budgeting (A2)  
→ Memory Gating (A3)  
→ Temporal Isolation (A4)  
→ Task Switching (A5)  
→ Policy  
→ Action  

---

## Demo Scenario

The demo simulates:
- Starting a main task thread
- Receiving an interrupting request
- Pausing the main thread with a resume snapshot
- Handling the interrupt thread
- Resuming the original task without drift
- Optional merging of related threads

Run:

```bash
python demo.py
