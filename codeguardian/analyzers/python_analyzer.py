"""Local Python analyzers for a checkout explicitly trusted by the operator."""

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import monotonic

from .base import AnalyzerPlan, IsolatedContext, RawResult, ReviewContext


@dataclass(frozen=True)
class PythonAnalyzer:
    id: str
    head_sha: str
    checkout: Path
    languages = ("python",)
    file_patterns = ("*.py", "*.pyi")
    requirements = ("Python 3.12+",)
    supports_untrusted_pr = False

    @property
    def version(self) -> str:
        try:
            return version(self.id)
        except PackageNotFoundError:
            return "unavailable"

    def supports(self, context: ReviewContext) -> bool:
        return self.id == "pytest" or bool(context.changed_files)

    def plan(self, context: ReviewContext) -> AnalyzerPlan:
        if self.id == "ruff":
            args = (
                "check",
                "--isolated",
                "--no-cache",
                "--output-format",
                "json",
                "--",
                *(str(path) for path in context.changed_files),
            )
            timeout = 30
        else:
            args = ("-p", "no:cacheprovider")
            timeout = 120
        return AnalyzerPlan(
            (sys.executable, "-I", "-B", "-m", self.id, *args),
            timeout,
            self.id in context.policy.required_checks,
        )

    def run(self, context: IsolatedContext) -> RawResult:
        start = monotonic()
        allowed = {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "COMSPEC"}
        env = {
            key: value for key, value in os.environ.items() if key.upper() in allowed
        }
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        try:
            result = subprocess.run(
                context.plan.command,
                cwd=context.checkout,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=context.plan.timeout_seconds,
            )
        except (OSError, subprocess.TimeoutExpired):
            return RawResult(None, "", "", int((monotonic() - start) * 1000))
        return RawResult(
            result.returncode,
            result.stdout,
            result.stderr,
            int((monotonic() - start) * 1000),
        )

    def finding(
        self, rule: str, title: str, path: str | None = None, line: int | None = None
    ) -> dict:
        fingerprint = hashlib.sha256(
            json.dumps([rule, path, line, title]).encode()
        ).hexdigest()
        result = {
            "schema_version": "1",
            "finding_id": fingerprint,
            "fingerprint": fingerprint,
            "rule_id": rule,
            "source": self.id,
            "severity": "high" if self.id == "pytest" else "low",
            "evidence_status": "verified",
            "title": title,
            "explanation": title,
            "recommendation": "Review the indicated check locally.",
            "head_sha": self.head_sha,
        }
        if path is not None:
            result.update(file=path, line=line)
        return result

    def normalize(self, raw_result: RawResult) -> dict:
        status, findings = "error", []
        if raw_result.exit_code == 0:
            status = "success"
        elif raw_result.exit_code == 1:
            if self.id == "pytest":
                findings = [
                    self.finding("CG-TEST-001", "pytest reported failing tests")
                ]
            else:
                try:
                    findings = [
                        self.finding(
                            "CG-STYLE-001",
                            f"Ruff {item['code']}",
                            (self.checkout / item["filename"])
                            .resolve()
                            .relative_to(self.checkout)
                            .as_posix(),
                            item["location"]["row"],
                        )
                        for item in json.loads(raw_result.stdout)
                    ]
                except (ValueError, KeyError, TypeError):
                    findings = []
            if findings:
                status = "findings"
        return {
            "tool": self.id,
            "version": self.version,
            "status": status,
            "duration_ms": raw_result.duration_ms,
            "findings": findings,
            "logs_artifact": None,
            "coverage_scope": [],
        }
