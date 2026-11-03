"""Run a technical review on a trusted local Python checkout."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from jsonschema import ValidationError

from codeguardian.analyzers.base import IsolatedContext, ReviewContext
from codeguardian.analyzers.python_analyzer import PythonAnalyzer
from codeguardian.core.config import PolicyInput, PolicySource, resolve_policy
from codeguardian.core.contracts import validate_contract
from codeguardian.core.inspector import changed_python


def review(root: Path, base: str, head: str, policy_path: Path) -> dict:
    policy_text = policy_path.read_text(encoding="utf-8")
    policy = resolve_policy(PolicyInput(policy_text, PolicySource.APPROVED))
    changed = changed_python(root, base, head)
    context = ReviewContext(changed, policy)
    results, failures, incomplete, advisories = [], [], [], []
    for tool in ("ruff", "pytest"):
        analyzer = PythonAnalyzer(tool, head, root)
        if not analyzer.supports(context):
            continue
        plan = analyzer.plan(context)
        result = analyzer.normalize(analyzer.run(IsolatedContext(root, plan)))
        if tool == "ruff":
            result["coverage_scope"] = [path.as_posix() for path in changed]
        else:
            result["coverage_scope"] = ["project"]
        validate_contract("analyzer-result", result)
        results.append(result)
        if result["status"] == "findings":
            (failures if plan.required else advisories).append(f"{tool}: findings")
        elif result["status"] == "error":
            (incomplete if plan.required else advisories).append(
                f"{tool}: execution incomplete"
            )

    status = "PASS"
    if failures:
        status = "FAIL"
    elif incomplete:
        status = "INCOMPLETE"
    elif advisories:
        status = "WARNING"
    decision = {
        "logical_status": status,
        "blocking_reasons": failures + incomplete,
        "advisories": advisories,
        "head_sha": head,
        "policy_version": hashlib.sha256(policy_text.encode()).hexdigest(),
        "required_checks": sorted(policy.required_checks),
    }
    validate_contract("quality-decision", decision)
    return {"decision": decision, "analyzers": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument(
        "--policy",
        required=True,
        type=Path,
        help="Approved policy file outside the target checkout",
    )
    parser.add_argument(
        "--trusted",
        required=True,
        action="store_true",
        help="Confirm the target repository and its test code are trusted",
    )
    args = parser.parse_args()
    root = args.checkout.resolve()
    if args.policy.resolve().is_relative_to(root):
        parser.error("Supply an approved policy outside the target checkout")
    try:
        report = review(root, args.base, args.head, args.policy)
    except (OSError, ValueError, ValidationError, subprocess.TimeoutExpired) as exc:
        print(
            json.dumps(
                {
                    "decision": {"logical_status": "INCOMPLETE", "head_sha": args.head},
                    "error": str(exc),
                }
            )
        )
        return 2
    print(json.dumps(report, indent=2))
    return {"FAIL": 1, "INCOMPLETE": 2}.get(report["decision"]["logical_status"], 0)


if __name__ == "__main__":
    raise SystemExit(main())
