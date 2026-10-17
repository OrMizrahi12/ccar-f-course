# Expected output: Lesson 7.4, Few-shot for messy documents

What each step showed in the lesson (Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The documents and their labels are the same for everyone (they ship in `data/invoices/`); what Claude reads from them varies from run to run, so compare the behavior, not every row.

## Step 1: measure

`git status --short` prints nothing (the tree is clean, at the Lesson 7.3 commit). Typing `dev_check.py` produces no output until you run it.

```text
$ python -m extraction.dev_check
INV-D01  table  ok
INV-D02  prose  ok
INV-D03  table  ok
INV-D04  email  ok
INV-D05  scan   ok
INV-D06  prose  line 1 unit 'roll' (label 'each'); line 2 unit 'roll' (label 'each')
INV-D07  table  line 1 quantity 1 (label 144); line 1 unit 'gross' (label 'each'); line 2 unit '' (label 'each'); line 3 unit '' (label 'each')
INV-D08  email  line 1 unit 'gross' (label 'each')
INV-D09  table  ok
INV-D10  email  ok
INV-D11  scan   ok
INV-D12  prose  ok
9 of 12 documents exact; 7 wrong values
```

The rows print one by one, as each document finishes (each runs Lesson 7.3's checks and retries, with their lines kept out of the table). The three failures are the informal quantities and units: D06's "roll" of packing tape and labels, D07's "1 gross" of desk lamps read as one, D08's "1 gross" of pillows with the unit `gross`, and two empty units. On your run the count may differ (in practice runs even more failed); what matters is that you now have a number to beat.

## Step 2: five examples

`mkdir` and the two files produce no output. `extract.py` now reads `prompts/examples.md` once, at import, and sends it with every request, between the rules and the document.

## Step 3: the same twelve documents again

```text
$ python -m extraction.dev_check
INV-D01  table  ok
INV-D02  prose  ok
INV-D03  table  ok
INV-D04  email  ok
INV-D05  scan   ok
INV-D06  prose  ok
INV-D07  table  ok
INV-D08  email  ok
INV-D09  table  ok
INV-D10  email  ok
INV-D11  scan   ok
INV-D12  prose  ok
12 of 12 documents exact; 0 wrong values
```

D06's units, D07's gross and D08's email all match their labels now. On yours, one row may still differ: run it again, and look at which layout it is. Two runs aren't a guarantee; Lessons 7.5 and 7.6 measure at scale.

## Commit and push

```text
$ git status --short
 M extraction/extract.py
?? extraction/dev_check.py
?? extraction/prompts/
$ git add extraction
$ git commit -m "Lesson 7.4: few-shot examples for messy documents, and a dev-set check against the labels"
[main cb00838] Lesson 7.4: few-shot examples for messy documents, and a dev-set check against the labels
 3 files changed, 92 insertions(+), 1 deletion(-)
 create mode 100644 extraction/dev_check.py
 create mode 100644 extraction/prompts/examples.md
```

`git push` ends with `main -> main`. Your hashes will differ.
