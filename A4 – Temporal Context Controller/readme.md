# A4 – Temporal Context Controller
_Attention & Context Controllers → Foundation Tier_

A4 introduces explicit temporal modes for AI agents.

If A1 decides:
> What context frame dominates?

If A2 decides:
> How much cognitive effort is allowed?

If A3 decides:
> Which memories are allowed into reasoning?

Then A4 decides:

> Are we recalling the past, acting in the present, or simulating the future?

Most agent systems blur temporal boundaries. They mix:
- Past memories
- Current world state
- Hypothetical simulations
- Planned futures

Without temporal control, agents:
- Leak simulated outcomes into real execution
- Confuse previous states with current conditions
- Overwrite present reality with imagined futures
- Lose coherence in long-horizon tasks

A4 prevents temporal contamination.

---

## Core Concept

The Temporal Context Controller enforces explicit operating modes:

### 1. RECALL Mode
Used for:
- Accessing episodic memory
- Reviewing past outcomes
- Extracting lessons

Rules:
- No world state mutation
- No policy execution
- Only read operations allowed

---

### 2. EXECUTION Mode
Used for:
- Acting in the present
- Tool invocation
- Real state updates

Rules:
- No hypothetical simulation writes
- Memory writes allowed
- Budget strictly enforced

---

### 3. SIMULATION Mode
Used for:
- Planning
- What-if reasoning
- Counterfactual evaluation
- Strategy testing

Rules:
- No real world mutation
- Simulation memory isolated
- Explicit promotion required before execution

---

## Temporal Isolation

Each mode maintains:

- Separate memory scope
- Separate write permissions
- Separate budget scaling (optional integration with A2)

Temporal isolation prevents:
- Future hallucinations affecting execution
- Retrospective bias overwriting state
- Planning artifacts leaking into real logs

---

## Core Components

### TemporalMode
Enum:
- RECALL
- EXECUTION
- SIMULATION

### TemporalController
- Switches modes
- Enforces allowed operations
- Blocks illegal state transitions

### SimulationSandbox
- Temporary state container
- Cleared after exit unless promoted

---

## Relationship to Previous Projects

A1:
> What context dominates?

A2:
> How much thinking is allowed?

A3:
> Which memories influence reasoning?

A4:
> In what time-mode is reasoning happening?

Together:

Perception  
→ Attention Framing (A1)  
→ Effort Allocation (A2)  
→ Memory Gating (A3)  
→ Temporal Mode Control (A4)  
→ Policy  
→ Action  

---

## Demo Scenario

The demo simulates:
- Switching between RECALL, EXECUTION, and SIMULATION
- Attempting illegal state mutations
- Simulation producing hypothetical outcomes
- Controlled promotion of simulation results to execution

Run:

```bash
python demo.py
