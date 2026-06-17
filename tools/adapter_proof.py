from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from execution.mock_adapter import execute_command


def run_case(name, decision_package):
    result = execute_command(decision_package)

    print(f"\n{name}")
    print("-" * len(name))
    print(f"decision: {result['decision']}")
    print(f"status: {result['status']}")
    print(f"hardware_action_executed: {result['hardware_action_executed']}")
    print(f"bounded: {result['bounded']}")
    for line in result["runtime_log"]:
        print(line)


BASE = {
    "request_id": "req-adapter-proof-001",
    "receipt_id": "rcpt-adapter-proof-001",
    "rule": "adapter_proof",
    "reason": "Adapter proof case",
    "execution_mode": {
        "action": "mock_action",
        "buffer_action": "HOLD_AND_NOTIFY",
    },
}

run_case(
    "ALLOW executes full mock action",
    {
        **BASE,
        "decision": "ALLOW",
    },
)

run_case(
    "RESTRICT executes bounded mock action",
    {
        **BASE,
        "decision": "RESTRICT",
    },
)

run_case(
    "DENY aborts mock action",
    {
        **BASE,
        "decision": "DENY",
    },
)
