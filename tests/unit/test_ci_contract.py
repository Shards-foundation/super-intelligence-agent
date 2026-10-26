"""Regression checks for the install failure and the CI test gate.

Default-branch CI stopped in `pip install -r requirements.txt` because
`moonshot-python` is not a PyPI distribution. The next install step,
`pip install .`, also failed: setuptools refused the flat layout. The test
step then masked pytest's exit code with `|| echo`.
"""

import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _requirement_names(text: str) -> list[str]:
    names = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        names.append(re.split(r"[<>=!\[]", line, maxsplit=1)[0].strip())
    return names


def test_requirements_do_not_depend_on_unpublished_moonshot_sdk():
    names = _requirement_names((ROOT / "requirements.txt").read_text())
    assert "moonshot-python" not in names
    assert "litellm" in names


def test_package_discovery_lists_import_roots_only():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    find = data["tool"]["setuptools"]["packages"]["find"]
    include = find["include"]
    for name in ("agents*", "api*", "core*", "memory*", "tools*"):
        assert name in include
    assert find["namespaces"] is True
    joined = " ".join(include)
    assert "deploy" not in joined
    assert "tests" not in joined


def test_project_wheel_metadata_builds():
    completed = subprocess.run(
        [sys.executable, "-m", "pip", "install", str(ROOT), "--no-deps", "--dry-run"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_ci_workflow_fails_when_pytest_fails():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
    assert "python -m pytest" in workflow
    assert "|| echo" not in workflow
    assert "E9,F63,F7,F82" in workflow


def test_dependabot_does_not_scan_a_missing_npm_manifest():
    config = (ROOT / ".github" / "dependabot.yml").read_text()
    assert 'package-ecosystem: "npm"' not in config
    assert 'package-ecosystem: "pip"' in config
    assert not (ROOT / "package.json").exists()
