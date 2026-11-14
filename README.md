# QA Automation Portfolio: PowderLine Board Sizer

Automated UI tests (Python + Playwright + pytest) for a snowboard size calculator, checked against a written product spec.

**Result:** 21 tests, 15 pass, 6 fail on 5 real bugs, which are filed below. The app is **not ready for release**.

## What's here
| Folder | What it is |
|---|---|
| `apps/` | The app under test, a practice app with bugs planted in it |
| `docs/SPEC.md` | The product spec (the "ticket") the tests are written against |
| `tests/` | Playwright test suite, organized by spec rule |
| `bug-reports/` | Bug reports for failures |
| `.github/workflows/` | CI: runs every test on each push |

## Bugs found
| ID | Severity | Bug | Spec rule |
|---|---|---|---|
| [BUG-001](bug-reports/BUG-001-pounds-conversion.md) | High | Pounds converted by ÷2 instead of ÷2.2046, so riders near 55 kg or 90 kg get the wrong board | #2, #5 |
| [BUG-002](bug-reports/BUG-002-powder-adjustment.md) | High | Powder style adds +2 cm instead of +4 cm | #3 |
| BUG-003 | Medium | Max height 220 cm is rejected (off-by-one boundary) | #6 |
| BUG-004 | Medium | Boot size exactly 11 gets no wide-board recommendation | #9 |
| BUG-005 | High | Empty weight returns a board size instead of an error | #8 |

Tests for known bugs are marked `xfail(strict=True)`, so CI stays green while the bug is open and flags the test the moment the bug is fixed.

## Test approach
- One test per user action, with the expected value worked out from the spec **before** running it
- **Boundary testing** at every cutoff: 55/90 kg, 120/220 cm, boot size 11
- Negative tests: out-of-range and empty fields must show an error, never a silent wrong answer

## Run it
```
pip install -r requirements.txt
playwright install chromium
pytest
```

## How I used AI
AI (Claude) helped write the test code, the practice app, and BUG-002, used openly, the way AI-assisted QA teams work. My part: working out and verifying expected results against the spec, triaging failures (real bug or bad test?), writing BUG-001, and reviewing everything before it ships.

## TypeScript version (in progress)
`ts-tests/` has the same tests being converted to TypeScript (`@playwright/test`), because many QA teams use TypeScript. The first test was converted with AI help and walked through line by line; the rest I am converting myself. Run with `cd ts-tests && npm install && npx playwright test`.

## Contact
Hudson Rowles, Environmental Engineering student at Montana State University. [LinkedIn](https://www.linkedin.com/in/hudson-rowles-a5b85844b/)
