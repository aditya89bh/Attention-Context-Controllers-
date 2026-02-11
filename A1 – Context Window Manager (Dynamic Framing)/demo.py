
---

## `A1_Context_Window_Manager/demo.py`

```python
from src.events import Event, EventType
from src.manager import ContextWindowManager
from src.rendering import pretty_print_snapshot


def run_demo() -> None:
    mgr = ContextWindowManager()

    mgr.set_goal(
        "Build A1 Context Window Manager demo and produce a bounded context window each step.",
        constraints=[
            "No external dependencies",
            "Prefer signal over noise",
            "Risk signals must override everything else",
        ],
    )

    # Step 1: baseline render
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 2: observation about system
    mgr.update(Event(EventType.OBSERVATION, {"text": "User wants A1 README then code. Keep outputs paste-friendly.", "urgency": 0.4}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 3: message arrives
    mgr.update(Event(EventType.MESSAGE, {"from": "user", "text": "Can you keep the code in one solid block? I hate split cells."}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 4: tool result arrives
    mgr.update(Event(EventType.TOOL_RESULT, {"tool": "repo_scaffold", "result": "Created /A1 folder structure and added README template."}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 5: deadline / urgency
    mgr.update(Event(EventType.OBSERVATION, {"text": "Milestone due by tonight: demo must run end-to-end.", "urgency": 0.9}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 6: risk flag
    mgr.update(Event(EventType.RISK_FLAG, {"reason": "Potential privacy issue: do not store sensitive personal data in context logs.", "level": 0.85}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))

    # Step 7: after risk handled, continue
    mgr.update(Event(EventType.NOTE, {"text": "Apply redaction rules in later versions (A6/A9)."}))
    pretty_print_snapshot(mgr.render_context(budget_chars=1400))


if __name__ == "__main__":
    print("A1 – Context Window Manager Demo\n" + "-" * 32)
    run_demo()
