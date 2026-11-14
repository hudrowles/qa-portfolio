# BUG-001 · Board length 3 cm too long when weight is entered in pounds

**Severity:** High. The customer is told to buy the wrong board: 157 cm instead of 154 cm.

**Steps to reproduce:**
1. Open `apps/snowboard-sizer.html` in a browser.
2. Enter Height: 178 cm, Weight: 120 with the unit set to lb, Style: "all", and leave Boot size blank.
3. Click the button that calculates the board size.

**Expected result:** Recommended board length is 154 cm. 120 lb is 54.4 kg, which is under 55 kg, so the board should be 3 cm shorter.

**Actual result:** Recommended board length is 157 cm.

**Spec rule broken:** "Riders under 55 kg get a board 3 cm shorter." (spec #2, with the conversion in spec #5)

**Notes / likely cause:** The app turns pounds into kilograms by dividing by 2 instead of 2.2. That makes 120 lb come out as 60 kg instead of 54.4 kg, so the under-55 kg rule never runs. Riders who enter about 110–121 lb get the wrong board, and anything else that depends on weight could also be wrong. To fix it, divide by 2.2046 (or multiply by 0.4536).

**Automated test:** `tests/test_board_sizer.py::test_pounds_light_rider` and `test_pounds_heavy_boundary`
