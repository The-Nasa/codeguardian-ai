"""Verify that the packaged Standard policy can be resolved."""

from pathlib import Path

from codeguardian.core.config import PolicyInput, PolicySource, resolve_policy


def test_repository_standard_policy_requires_pytest():
    config = Path(__file__).resolve().parents[1] / "codeguardian.yml"
    policy = resolve_policy(
        PolicyInput(config.read_text(encoding="utf-8"), PolicySource.APPROVED)
    )
    assert policy.profile == "standard"
    assert "pytest" in policy.required_checks
    assert False, 'Intentional failure to verify the GitHub quality gate'
