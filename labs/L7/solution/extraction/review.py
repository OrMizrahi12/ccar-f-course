"""How good is the batch, slice by slice, and which records does a person check?

python -m extraction.review

Compares runs/batch.jsonl with labels.jsonl: overall, by layout and by field. A field's accuracy
in a layout is its confidence. Claude also rates four fields high or low; calibrate() measures how
often each rating was right. A record goes to a person when the batch flagged it, or when one of its
fields is weak: below TARGET in its layout, rated low, or rated at a level that is right less than
TARGET of the time. Of the rest, SAMPLE per layout are picked at random.
"""

import json
import random
from collections import defaultdict

from extraction.dev_check import same
from harborline.config import DATA_DIR, ROOT_DIR

FIELDS = ("supplier_name", "invoice_number", "invoice_date", "due_date", "payment_terms", "po_number", "currency",
          "subtotal", "tax", "shipping", "stated_total")
TARGET = 0.95  # a field this accurate in its layout is trusted without a person
SAMPLE = 2  # trusted records per layout that a person checks anyway


def compare(record, label):
    """(field, right) for every value the label has an answer for."""
    if record["status"] == "skipped":
        return [("doc_type", record.get("doc_type") == label["doc_type"])]
    pairs = [(field, same(record.get(field), label[field])) for field in FIELDS]
    lines = record.get("line_items", [])
    pairs.append(("line count", len(lines) == len(label["line_items"])))
    for got, want in zip(lines, label["line_items"]):
        pairs += [(f"line {key}", same(got[key], want[key])) for key in ("quantity", "unit", "unit_price", "amount")]
    return pairs


def accuracy(pairs):
    return sum(right for _, right in pairs) / len(pairs)


def calibrate(records, labels):
    """(field, Claude's rating) -> the (field, right) pairs for every record that rated that field."""
    table = defaultdict(list)
    for doc, record in records.items():
        for field, level in (record.get("confidence") or {}).items():
            table[field, level].append((field, same(record.get(field), labels[doc][field])))
    return table


def weak_fields(record, layout_low, calibration):
    """The fields of one record a person should check, and why."""
    weak = {field: f"{field} in this layout" for field in layout_low if field in record}
    for field, level in (record.get("confidence") or {}).items():
        if level == "low":
            weak[field] = f"{field} rated low"
        elif field in record and accuracy(calibration[field, level]) < TARGET:
            weak[field] = f"{field} rated {level}, right {accuracy(calibration[field, level]):.0%} of the time"
    return sorted(weak.values())


def main():
    labels = {label["doc_id"]: label for label in map(json.loads, (DATA_DIR / "invoices" / "labels.jsonl").open())}
    records = {record["doc_id"]: record for record in map(json.loads, (ROOT_DIR / "runs" / "batch.jsonl").open())}
    layout = {doc: labels[doc]["format"] for doc in records}  # this month is labeled, layout included
    results = {doc: compare(record, labels[doc]) for doc, record in records.items()}

    everything = [pair for pairs in results.values() for pair in pairs]
    print(f"overall {accuracy(everything):.1%} of {len(everything)} values")
    by_layout, by_field, confidence = defaultdict(list), defaultdict(list), defaultdict(list)
    for doc, pairs in results.items():
        for field, right in pairs:
            by_layout[layout[doc]].append((field, right))
            by_field[field].append((field, right))
            confidence[layout[doc], field].append((field, right))
    for name, pairs in sorted(by_layout.items()):
        print(f"  {name:6} {accuracy(pairs):.1%}")
    for name, pairs in sorted(by_field.items(), key=lambda item: accuracy(item[1])):
        if accuracy(pairs) < 1:  # the fields that were always right add nothing here
            print(f"  {name:14} {accuracy(pairs):.1%}")
    low = {key: accuracy(pairs) for key, pairs in confidence.items() if accuracy(pairs) < TARGET}
    print("below target:", "; ".join(f"{field} in {name} {value:.0%}" for (name, field), value in sorted(low.items())))

    calibration = calibrate(records, labels)
    for (field, level), pairs in sorted(calibration.items()):
        print(f"  rated {level:4} {field:14} right {accuracy(pairs):.0%} of {len(pairs)}")

    queue, trusted = [], defaultdict(list)
    for doc, record in sorted(records.items()):
        if record["status"] == "skipped":  # not an invoice: nothing to check field by field
            continue
        weak = weak_fields(record, [field for (name, field) in low if name == layout[doc]], calibration)
        if record["status"].startswith("review"):
            queue.append({"doc_id": doc, "why": record["status"]})
        elif weak:
            queue.append({"doc_id": doc, "why": "low confidence: " + "; ".join(weak)})
        elif record["status"] == "ok":
            trusted[layout[doc]].append(doc)
    for name, docs in sorted(trusted.items()):
        for doc in random.sample(docs, min(SAMPLE, len(docs))):
            queue.append({"doc_id": doc, "why": f"random sample of {name}"})

    with (ROOT_DIR / "runs" / "review_queue.jsonl").open("w") as out:
        out.writelines(json.dumps(item) + "\n" for item in queue)
    whys = [item["why"].split(":")[0] for item in queue]
    for why in sorted(set(whys)):
        print(f"{whys.count(why):3}  {why}")
    missed = sum(not right for docs in trusted.values() for doc in docs for _, right in results[doc])
    count = sum(map(len, trusted.values()))
    print(f"{count} records trusted; {missed} wrong values among them: the samples estimate this")


if __name__ == "__main__":
    main()
