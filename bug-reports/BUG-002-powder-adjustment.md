# BUG-002 · Powder style adds 2 cm instead of 4 cm, recommending a board that's too short

**Severity:** High. Every rider who picks Powder gets a board 2 cm shorter than the spec says, so the store recommends the wrong product for a whole riding style.

**Steps to reproduce:**
1. Open `apps/snowboard-sizer.html` in a browser.
2. Enter Height: 178 cm, Weight: 75 kg, Style: "Powder", and leave Boot size blank.
3. Click **Find my board**.

**Expected result:** Recommended length: **161 cm**. Base 178 × 0.88 = 156.6 cm, 75 kg needs no weight adjustment, and Powder adds 4 cm: 156.6 + 4 = 160.6, which rounds to 161.

**Actual result:** Recommended length: **159 cm** (156.6 + 2 = 158.6, which rounds to 159).

**Spec rule broken:** #3, "Style adjustment: Freestyle = -2 cm, Powder = +4 cm, All-mountain = no change"

**Notes / likely cause:** The Powder adjustment in the code is `+2` instead of `+4`. It looks like a copy of the Freestyle line (which uses 2) with only the sign changed. Freestyle (-2) and All-mountain (0) are both correct. This affects 100% of Powder riders at any height and weight, so it isn't limited to a boundary case.

**Automated test:** `tests/test_board_sizer.py::test_powder_is_4cm_longer`
