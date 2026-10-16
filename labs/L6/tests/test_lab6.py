"""Lab 6: the CI review, hardened.

Checks ci/review.py with fake findings, fake earlier comments and a fake Claude. No key, no cost,
no GitHub.
"""

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ci_review", ROOT / "ci" / "review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def finding(**changes):
    base = {"path": "harborline/policy.py", "line": 12, "category": "bug", "severity": "high", "status": "new",
            "detected_pattern": "refund-by-hand", "issue": "The refund is computed by hand.",
            "fix": "Use refund_amount().", "confidence": 0.95}
    return base | changes


# A: the review payload, built without GitHub

def test_payload_puts_sure_findings_on_diff_lines_and_lists_the_rest():
    lines = {"harborline/policy.py": {10, 11, 12, 13}}
    new = [finding(), finding(line=40, issue="Off the diff."), finding(line=11, confidence=0.5, issue="Unsure.")]
    still = [finding(line=13, status="still_open", issue="Still there.")]
    body = review.payload(new, still, 2, lines)
    assert [c["line"] for c in body["comments"]] == [12]
    comment = body["comments"][0]
    assert review.MARK in comment["body"] and "refund-by-hand" in comment["body"]
    assert comment["side"] == "RIGHT" and body["event"] == "COMMENT"
    assert body["body"].startswith("Claude review: 3 new, 1 still open, 2 fixed.")
    assert "Off the diff." in body["body"] and "Unsure." in body["body"] and "Still there." in body["body"]


# B: a still_open the earlier comments don't back is new

def test_reconcile_keeps_still_open_only_when_an_earlier_comment_matches():
    prior = [{"path": "harborline/policy.py", "line": 10, "text": "**high · bug** `refund-by-hand`: ..."},
             {"path": "scripts/weekly_fees.py", "line": 30, "text": "**medium · bug** `cents-printed-as-dollars`: ..."}]
    near = finding(status="still_open", line=12)                       # within 3 lines of an earlier comment
    moved = finding(status="still_open", path="scripts/weekly_fees.py", line=80,
                    detected_pattern="cents-printed-as-dollars")        # moved, same pattern, same file
    unknown = finding(status="still_open", path="harborline/costs.py")  # no earlier comment at all
    fresh = finding()
    result = review.reconcile([near, moved, unknown, fresh], prior)
    assert [f["status"] for f in result] == ["still_open", "still_open", "new", "new"]


# C: patterns the team dismisses are dropped before the check pass

def test_skip_patterns_drop_findings_before_the_check(monkeypatch):
    config = json.loads((ROOT / "ci" / "review_config.json").read_text())
    assert isinstance(config["skip_patterns"], list)
    monkeypatch.setitem(review.CONFIG, "skip_patterns", ["raw-date-parse"])
    seen = []

    def fake_claude(prompt, text, schema):
        if schema == review.VERIFY:
            listed = re.findall(r"^(\d+)\. ", prompt, re.M)
            seen.extend(listed)
            return {"structured_output": {"checks": [{"index": int(i), "verdict": "confirmed", "confidence": 0.9}
                                                     for i in listed]}, "num_turns": 1, "total_cost_usd": 0.001}
        found = [finding(), finding(line=20, detected_pattern="raw-date-parse", issue="Parses dates by hand.")]
        return {"structured_output": {"findings": found}, "num_turns": 2, "total_cost_usd": 0.002}

    monkeypatch.setattr(review, "claude", fake_claude)
    diff = "diff --git a/harborline/policy.py b/harborline/policy.py\n+++ b/harborline/policy.py\n@@ -1 +1 @@\n+x\n"
    result = review.review(diff, [])
    assert [f["detected_pattern"] for f in result["findings"]] == ["refund-by-hand"]
    assert seen == ["0"], "the skipped finding reached the check pass"


# D: generated tests for policy.py, reviewed and kept

def test_generated_policy_tests_exist():
    path = ROOT / "tests" / "test_policy_generated.py"
    assert path.exists(), "run ci/testgen.py harborline/policy.py and keep the tests you reviewed"
    assert re.search(r"^def test_", path.read_text(), re.M)
