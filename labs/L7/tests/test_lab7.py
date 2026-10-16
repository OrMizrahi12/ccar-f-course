"""Lab 7: the extraction pipeline, finished.

Checks the schema, the retry log, the batch helpers, review routing and the examples with fake
records and a fake model. No key, no cost.
"""

import json
import re
from pathlib import Path

import pytest

from extraction import batch, dev_check, review, schema, validate
from extraction.extract import RECORD_DOCUMENT

ROOT = Path(__file__).resolve().parent.parent
LEVELS = {"high", "low"}


def record(**changes):
    """A record that passes every check: one line, totals that agree, all four fields rated high."""
    base = {"supplier_name": "Ironleaf Tools Inc.", "invoice_number": "ILT-1", "invoice_date": "2026-07-03",
            "due_date": "2026-08-02", "payment_terms": "Net 30", "po_number": None, "currency": "USD",
            "line_items": [{"description": "Desk lamp", "quantity": 6, "unit": "each", "unit_price": 19.7,
                            "amount": 118.2}],
            "subtotal": 118.2, "tax": 0, "shipping": 0, "stated_total": 118.2,
            "confidence": {"supplier_name": "high", "invoice_date": "high", "due_date": "high",
                           "stated_total": "high"}}
    return base | changes


# A: field-level confidence from Claude, calibrated on the labels

def test_the_record_carries_field_level_confidence():
    fields = schema.Confidence.model_fields
    assert {"supplier_name", "invoice_date", "due_date", "stated_total"} <= set(fields)
    for name in fields:
        assert set(fields[name].annotation.__args__) == LEVELS, f"{name} must be rated high or low"
    assert "confidence" in RECORD_DOCUMENT["input_schema"]["required"]
    schema.Document.model_validate(record())


def test_calibration_measures_each_rating_and_routes_weak_fields():
    records = {"A": record(), "B": record(supplier_name="IRONLEAF TOOLS INC."), "C": record()}
    labels = {doc: record() for doc in records}
    calibration = review.calibrate(records, labels)
    assert review.accuracy(calibration["supplier_name", "high"]) == pytest.approx(2 / 3)
    assert review.accuracy(calibration["stated_total", "high"]) == 1
    # rated high, but high is right only 67% of the time for supplier_name: a person checks it
    weak = review.weak_fields(records["A"], [], calibration)
    assert len(weak) == 1 and weak[0].startswith("supplier_name")
    # rated low: always checked
    low = record(confidence=record()["confidence"] | {"due_date": "low"})
    assert any(reason.startswith("due_date") for reason in review.weak_fields(low, [], calibration))
    # a field weak in this layout is checked even when Claude rates it high
    good = {key: [("x", True)] * 10 for key in calibration}
    assert review.weak_fields(record(), ["invoice_number"], good) == ["invoice_number in this layout"]


# B: the retry log: which failures a retry fixed, and which it didn't

def fake_calls(*replies):
    replies = iter(replies)
    return lambda client, text, tool, note="": next(replies)


META = {"doc_type": "invoice", "doc_type_detail": None, "supplier_name": "Ironleaf Tools Inc."}
MISREAD = record(line_items=[{"description": "Desk lamp", "quantity": 1, "unit": "gross", "unit_price": 19.7,
                              "amount": 118.2}])


def test_the_retry_log_records_a_failure_a_retry_fixed(monkeypatch):
    monkeypatch.setattr(validate, "call", fake_calls(META, MISREAD, record()))
    result = validate.extract_checked(None, ROOT / "data/invoices/dev/INV-D08.txt")
    assert result["status"] == "ok"
    assert result["retry_log"] == [{"attempt": 1, "kinds": ["line arithmetic"], "resolved": True}]


def test_the_retry_log_records_failures_no_retry_fixed(monkeypatch):
    bad_date = record(invoice_date="03/07/2026")
    monkeypatch.setattr(validate, "call", fake_calls(META, MISREAD, MISREAD, bad_date))
    result = validate.extract_checked(None, ROOT / "data/invoices/dev/INV-D08.txt")
    assert result["status"].startswith("review: still failing")
    assert [entry["kinds"] for entry in result["retry_log"]] == [["line arithmetic"], ["line arithmetic"],
                                                                   ["date format"]]
    assert not any(entry["resolved"] for entry in result["retry_log"])


def test_a_missing_total_is_never_retried(monkeypatch):
    monkeypatch.setattr(validate, "call", fake_calls(META, record(stated_total=None)))
    result = validate.extract_checked(None, ROOT / "data/invoices/dev/INV-D11.txt")
    assert result["status"] == "review: the document states no total"
    assert result["retry_log"] == []


# C: the SLA and long documents

def test_submit_every_leaves_room_for_the_slowest_batch():
    assert batch.submit_every(36) == 8
    assert batch.submit_every(48, margin_hours=6) == 18
    with pytest.raises(ValueError):
        batch.submit_every(24)


def test_parts_splits_a_table_and_leaves_other_layouts_whole():
    text = (ROOT / "data/invoices/batch/INV-0008.txt").read_text()
    pieces = batch.parts(text)
    assert len(pieces) == 19
    assert all("TOTAL DUE" in piece and "Invoice No" in piece for piece in pieces)
    letter = "Dear Harborline,\nWe supplied 4 desk fans at $22.00 each.\nTotal due: $88.00\n"
    assert batch.parts(letter) == [letter]


# D: an example for names in capitals, and the dev check compares names

def test_the_examples_are_well_formed_and_cover_names_in_capitals():
    text = (ROOT / "extraction/prompts/examples.md").read_text()
    examples = re.findall(r"<example>(.*?)</example>", text, re.S)
    assert len(examples) >= 6
    names = []
    for example in examples:
        assert "<document>" in example and "<why>" in example
        for line_item in re.findall(r"<line_item>(.*?)</line_item>", example, re.S):
            schema.LineItem.model_validate_json(line_item)
        for fields in re.findall(r"<fields>(.*?)</fields>", example, re.S):
            values = schema.Document.model_validate_json(record_json(fields))
            names.append(values.supplier_name)
    assert any(name != name.upper() and name.upper() in text for name in names), \
        "no example turns a name printed in capitals into the way the company writes it"
    assert "supplier_name" in dev_check.FIELDS


def record_json(fields):
    """The example's fields on top of a valid record, as JSON."""
    return json.dumps(record() | {"supplier_name": "?"} | json.loads(fields))
