import subprocess

import pytest

from codeguardian.review import review


@pytest.mark.parametrize(
    ("source", "suite", "expected"),
    [
        ("value = 1", "def test_ok(): assert True", "PASS"),
        ("import os", "def test_ok(): assert True", "WARNING"),
        ("value = 1", "def test_bad(): assert False", "FAIL"),
        ("value = 1", "", "INCOMPLETE"),
    ],
)
def test_review_with_real_tools(tmp_path, source, suite, expected):
    checkout = tmp_path / "checkout"
    checkout.mkdir()

    def git(*args):
        return subprocess.check_output(
            (
                "git",
                "-c",
                "user.name=CodeGuardian Test",
                "-c",
                "user.email=test@example.invalid",
                "-c",
                "commit.gpgsign=false",
                *args,
            ),
            cwd=checkout,
            text=True,
        ).strip()

    git("init", "-q")
    git("commit", "-q", "--allow-empty", "-m", "base")
    base = git("rev-parse", "HEAD")
    (checkout / "demo.py").write_text(source + "\n", encoding="utf-8")
    (checkout / "test_demo.py").write_text(suite + "\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-qm", "head")
    head = git("rev-parse", "HEAD")
    policy = tmp_path / "approved.yml"
    policy.write_text(
        "version: 1\nprofile: standard\nrequired_checks: [pytest]\n"
        "allow_external_tests: false\n",
        encoding="utf-8",
    )

    report = review(checkout, base, head, policy)
    assert report["decision"]["logical_status"] == expected
    assert report["decision"]["head_sha"] == head
    if expected == "WARNING":
        assert report["analyzers"][0]["findings"][0]["file"] == "demo.py"
