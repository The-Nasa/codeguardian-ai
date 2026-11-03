"""Resolve Standard policy from inputs whose provenance the caller verifies."""

from dataclasses import dataclass
from enum import Enum

import yaml
from jsonschema import ValidationError

from .contracts import validate_contract


class PolicyError(ValueError):
    pass


class PolicySource(Enum):
    APPROVED = "approved"
    PULL_REQUEST = "pull_request"


class StrictLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in mapping:
                raise PolicyError("Policy keys must be unique strings")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


@dataclass(frozen=True)
class PolicyInput:
    content: str
    source: PolicySource


@dataclass(frozen=True)
class EffectivePolicy:
    profile: str
    required_checks: frozenset[str]
    allow_external_tests: bool


def _read_policy(policy: PolicyInput) -> EffectivePolicy:
    if policy.source is not PolicySource.APPROVED:
        raise PolicyError("Policy must come from an approved source")
    try:
        data = yaml.load(policy.content, Loader=StrictLoader)
        validate_contract("config", data)
    except (yaml.YAMLError, ValidationError, RecursionError):
        raise PolicyError("Invalid Standard policy") from None
    if data["allow_external_tests"]:
        raise PolicyError("External dynamic tests are disabled")
    return EffectivePolicy(
        data["profile"], frozenset(data["required_checks"]), False
    )


def resolve_policy(
    organization: PolicyInput,
    language: PolicyInput | None = None,
    repository: PolicyInput | None = None,
) -> EffectivePolicy:
    effective = _read_policy(organization)
    if "pytest" not in effective.required_checks:
        raise PolicyError("Standard requires pytest")
    for layer in (language, repository):
        if layer is None:
            continue
        candidate = _read_policy(layer)
        if not effective.required_checks <= candidate.required_checks:
            raise PolicyError("Policy cannot remove inherited required checks")
        effective = candidate
    return effective
