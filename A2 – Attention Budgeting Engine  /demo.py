from src.budget import AttentionBudget
from src.cost_model import CostModel, Operation
from src.controller import BudgetController
from src.rendering import print_header, print_event, print_summary


def run_demo() -> None:
    print_header("A2 – Attention Budgeting Engine Demo")

    # 1) Create budget + cost model + controller
    budget = AttentionBudget(total_units=60)
    cost_model = CostModel.default()
    ctrl = BudgetController(budget=budget, cost_model=cost_model)

    print_event("INIT", f"Total budget: {budget.total_units} units | Mode: {budget.mode.value}")

    # 2) Simulate a typical agent loop
    steps = [
        (Operation.RENDER_CONTEXT, "Render context window"),
        (Operation.REASON_STEP, "Reasoning step 1"),
        (Operation.MEMORY_RETRIEVAL, "Retrieve top memories"),
        (Operation.REASON_STEP, "Reasoning step 2"),
        (Operation.TOOL_CALL, "Call a tool (search/db/api)"),
        (Operation.REASON_STEP, "Reasoning step 3"),
        (Operation.MEMORY_RETRIEVAL, "Retrieve follow-up memories"),
        (Operation.RENDER_CONTEXT, "Re-render context window"),
        (Operation.TOOL_CALL, "Call tool again"),
        (Operation.REASON_STEP, "Reasoning step 4"),
        (Operation.REASON_STEP, "Reasoning step 5"),
        (Operation.RENDER_CONTEXT, "Final render"),
    ]

    for op, label in steps:
        result = ctrl.spend(op, meta={"label": label})
        print_event(
            "SPEND",
            f"{op.value:16s} | cost={result.cost:>2d} | remaining={result.remaining:>2d} "
            f"| mode={result.mode.value:12s} | allowed={result.allowed}"
        )

        # Demonstrate how budget mode influences behavior decisions
        if op == Operation.MEMORY_RETRIEVAL:
            print_event("POLICY", f"Memory top-k allowed right now: k={ctrl.max_memory_k()}")

        if op == Operation.TOOL_CALL:
            print_event("POLICY", f"Tool calls allowed right now: {ctrl.allow_tool_calls()}")

        if not result.allowed:
            print_event("STOP", "Budget exhausted: agent should stop, summarize, or switch to heuristic exit.")
            break

    # 3) Summary
    print_summary(budget, ctrl)


if __name__ == "__main__":
    run_demo()
