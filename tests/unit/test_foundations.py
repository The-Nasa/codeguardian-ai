import pytest
from jsonschema import ValidationError

from codeguardian.core.config import (
    PolicyError,
    PolicyInput,
    PolicySource,
    resolve_policy,
)
from codeguardian.core.contracts import validate_contract


def policy(checks="pytest", extra="", source=PolicySource.APPROVED):
    return PolicyInput(
        f"version: 1\nprofile: standard\nrequired_checks: [{checks}]\n"
        f"allow_external_tests: false\n{extra}",
        source,
    )


def test_repository_can_add_required_checks():
    result = resolve_policy(policy(), repository=policy("pytest, ruff"))
    assert result.required_checks == {"pytest", "ruff"}


@pytest.mark.parametrize(
    "candidate",
    [
        policy(source=PolicySource.PULL_REQUEST),
        policy("ruff"),
        policy(extra="unknown: true"),
        policy(extra="allow_external_tests: true"),
        policy(extra="profile: standard"),
    ],
)
def test_repository_cannot_replace_protected_policy(candidate):
    with pytest.raises(PolicyError):
        resolve_policy(policy(), repository=candidate)


@pytest.mark.parametrize("status", ["success", "findings", "error", "skipped"])
def test_analyzer_result_contract(status):
    result = {
        "tool": "ruff",
        "version": "demo",
        "status": status,
        "duration_ms": 0,
        "findings": [],
        "coverage_scope": ["demo.py"],
        "logs_artifact": None,
    }
    validate_contract("analyzer-result", result)
    with pytest.raises(ValidationError):
        validate_contract("analyzer-result", {**result, "duration_ms": "0"})
    with pytest.raises(ValidationError):
        validate_contract("analyzer-result", {**result, "status": "PASS"})


@pytest.mark.parametrize("evidence", ["verified", "suspected", "unverified"])
def test_finding_contract_preserves_evidence(evidence):
    finding = {
        "schema_version": "1",
        "finding_id": "demo",
        "fingerprint": "demo",
        "rule_id": "CG-STYLE-001",
        "source": "demo",
        "severity": "low",
        "evidence_status": evidence,
        "title": "Demo",
        "explanation": "Demo",
        "recommendation": "Demo",
        "head_sha": "a" * 40,
    }
    validate_contract("finding", finding)
    finding.pop("head_sha")
    with pytest.raises(ValidationError):
        validate_contract("finding", finding)
