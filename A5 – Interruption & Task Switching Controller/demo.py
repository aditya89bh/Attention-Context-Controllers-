from src.events import Event, EventType, Priority
from src.controller import TaskSwitchController
from src.rendering import print_header, print_state, print_log


def run_demo() -> None:
    print_header("A5 – Interruption & Task Switching Controller Demo")

    ctrl = TaskSwitchController()

    # Start a main thread
    ctrl.handle(Event(EventType.NEW_TASK, {"goal": "Implement A5 for GitHub and run demo in Colab"}, priority=Priority.NORMAL))
    print_state("After NEW_TASK (main)", ctrl)

    # Progress a bit
    ctrl.handle(Event(EventType.PROGRESS, {"note": "Created repo skeleton and README"}, priority=Priority.LOW))
    ctrl.handle(Event(EventType.PROGRESS, {"note": "Drafted controller API and thread lifecycle"}, priority=Priority.NORMAL))
    print_state("After PROGRESS (main)", ctrl)

    # Minor interruption: add to current thread
    ctrl.handle(Event(EventType.MESSAGE, {"from": "user", "text": "Keep the code modular, please."}, priority=Priority.LOW))
    print_state("After minor MESSAGE (stays on main)", ctrl)

    # Blocking interruption: urgent request comes in
    ctrl.handle(Event(EventType.INTERRUPT, {"goal": "Fix a broken import error in Colab for another project"}, priority=Priority.HIGH))
    print_state("After HIGH interrupt (main paused, interrupt active)", ctrl)

    # Do work on interrupt thread
    ctrl.handle(Event(EventType.PROGRESS, {"note": "Diagnosed: user executed src file directly, should run demo.py"}, priority=Priority.NORMAL))
    ctrl.handle(Event(EventType.DONE, {"summary": "Provided correct Colab workflow + fixed import path issue."}, priority=Priority.NORMAL))
    print_state("After DONE (interrupt)", ctrl)

    # Resume main thread
    ctrl.resume_previous()
    print_state("After resume_previous() (back to main)", ctrl)

    # Critical interruption: risk flag should override everything
    ctrl.handle(Event(EventType.RISK_FLAG, {"reason": "Potential leakage of private user data in logs"}, priority=Priority.CRITICAL))
    print_state("After CRITICAL risk (overrides, creates critical thread)", ctrl)

    # Resolve critical thread and return
    ctrl.handle(Event(EventType.DONE, {"summary": "Added rule: never store sensitive personal data; redact logs."}, priority=Priority.NORMAL))
    ctrl.resume_previous()
    print_state("After resolving risk + resume main", ctrl)

    # Finish main task
    ctrl.handle(Event(EventType.DONE, {"summary": "A5 implemented, demo runnable, ready for GitHub push."}, priority=Priority.NORMAL))
    print_state("After DONE (main)", ctrl)

    print_log(ctrl)


if __name__ == "__main__":
    run_demo()
