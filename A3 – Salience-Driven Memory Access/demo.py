from src.budget_adapter import BudgetMode
from src.memory import MemoryItem, MemoryStore
from src.salience import SalienceConfig, SalienceScorer
from src.gate import MemoryGate
from src.rendering import print_header, print_selected


def run_demo() -> None:
    print_header("A3 – Salience-Driven Memory Access Demo")

    # 1) Build a toy memory store
    store = MemoryStore()
    store.add(MemoryItem("User prefers modular repo structure", tags=("repo", "architecture"), risk=0.1, base_relevance=0.55, age_steps=8))
    store.add(MemoryItem("Tool calls are expensive; limit them when budget is low", tags=("budget", "tools"), risk=0.2, base_relevance=0.60, age_steps=3))
    store.add(MemoryItem("Avoid storing sensitive personal data in logs", tags=("privacy", "risk"), risk=0.95, base_relevance=0.35, age_steps=2))
    store.add(MemoryItem("Current goal: build A3 memory gating integrated with A2 budget mode", tags=("goal", "task"), risk=0.1, base_relevance=0.80, age_steps=1))
    store.add(MemoryItem("Old irrelevant detail about a past demo", tags=("misc",), risk=0.0, base_relevance=0.10, age_steps=30))
    store.add(MemoryItem("If deadline is near, prioritize action-oriented memories", tags=("temporal", "deadline"), risk=0.1, base_relevance=0.50, age_steps=4))

    # 2) Configure salience scoring
    cfg = SalienceConfig(
        w_base=0.45,
        w_recency=0.25,
        w_task=0.20,
        w_risk=0.10,  # risk can be made higher if you want risk to dominate
        recency_half_life_steps=12,
    )
    scorer = SalienceScorer(cfg)

    # 3) Gate uses budget mode to decide how many memories can enter reasoning
    gate = MemoryGate(scorer=scorer)

    task_query = "build A3 salience-driven memory access and integrate with A2 budgeting"
    foreground_frame = "TASK"

    # CASE A: FULL budget (like early in episode)
    selected_full = gate.select(
        candidates=store.all(),
        task_query=task_query,
        foreground_frame=foreground_frame,
        budget_mode=BudgetMode.FULL,
    )
    print_selected("CASE A: BudgetMode=FULL", selected_full)

    # CASE B: CONSERVATIVE budget
    selected_cons = gate.select(
        candidates=store.all(),
        task_query=task_query,
        foreground_frame=foreground_frame,
        budget_mode=BudgetMode.CONSERVATIVE,
    )
    print_selected("CASE B: BudgetMode=CONSERVATIVE", selected_cons)

    # CASE C: CRITICAL budget (late in episode)
    selected_crit = gate.select(
        candidates=store.all(),
        task_query=task_query,
        foreground_frame=foreground_frame,
        budget_mode=BudgetMode.CRITICAL,
    )
    print_selected("CASE C: BudgetMode=CRITICAL", selected_crit)

    # CASE D: Risk spike (simulate risk taking priority)
    # Increase risk weight to show "risk overrides similarity"
    scorer_risk = SalienceScorer(cfg.replace(w_risk=0.40, w_base=0.35))
    gate_risk = MemoryGate(scorer=scorer_risk)

    selected_risk = gate_risk.select(
        candidates=store.all(),
        task_query=task_query,
        foreground_frame=foreground_frame,
        budget_mode=BudgetMode.CONSERVATIVE,
    )
    print_selected("CASE D: Risk-heavy scoring (risk boosted)", selected_risk)


if __name__ == "__main__":
    run_demo()
