from src.temporal import TemporalController, TemporalMode, TemporalViolation
from src.ops import Op
from src.rendering import print_header, print_state, print_log


def run_demo() -> None:
    print_header("A4 – Temporal Context Controller Demo")

    ctrl = TemporalController()

    print_state("Initial", ctrl)

    # 1) RECALL mode: read-only, no world mutation, no tool calls
    ctrl.set_mode(TemporalMode.RECALL, reason="Need to check past events before acting")
    print_state("Switched to RECALL", ctrl)

    ctrl.log_event("Recall: last user request was to keep temporal isolation pure.")
    print_log(ctrl)

    try:
        ctrl.apply(Op.WORLD_MUTATION, {"set": {"status": "changed"}})
    except TemporalViolation as e:
        print(f"\nEXPECTED BLOCK (RECALL): {e}")

    try:
        ctrl.apply(Op.TOOL_CALL, {"tool": "web.search", "q": "anything"})
    except TemporalViolation as e:
        print(f"EXPECTED BLOCK (RECALL): {e}")

    # 2) SIMULATION mode: sandboxed changes allowed, but cannot touch real world
    ctrl.set_mode(TemporalMode.SIMULATION, reason="Try a plan before execution")
    print_state("Switched to SIMULATION", ctrl)

    ctrl.apply(Op.SIM_WRITE, {"set": {"plan": "Use minimal files, then add tests"}})
    ctrl.apply(Op.SIM_WRITE, {"set": {"predicted_outcome": "Fast iteration, no temporal leakage"}})
    ctrl.apply(Op.SIM_WRITE, {"set": {"risk_note": "Ensure simulation never mutates real state"}})
    print_state("After SIM writes", ctrl)

    try:
        ctrl.apply(Op.WORLD_MUTATION, {"set": {"should_not": "happen"}})
    except TemporalViolation as e:
        print(f"\nEXPECTED BLOCK (SIMULATION): {e}")

    # Promote simulation results explicitly (commit)
    ctrl.commit_simulation(keys=["plan", "predicted_outcome"])
    print_state("After COMMIT (promoted selected sim keys)", ctrl)

    # 3) EXECUTION mode: can mutate real world and write memories
    ctrl.set_mode(TemporalMode.EXECUTION, reason="Now we act")
    print_state("Switched to EXECUTION", ctrl)

    ctrl.apply(Op.WORLD_MUTATION, {"set": {"status": "executing", "step": 1}})
    ctrl.apply(Op.MEMORY_WRITE, {"append": "Executed plan step 1 successfully."})
    ctrl.apply(Op.TOOL_CALL, {"tool": "local.fs", "action": "write_files"})
    print_state("After EXECUTION operations", ctrl)

    # Simulation state should be isolated and still exists until cleared
    ctrl.clear_simulation()
    print_state("After clearing simulation sandbox", ctrl)

    print_log(ctrl)


if __name__ == "__main__":
    run_demo()
