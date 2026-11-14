# PowderLine Board Sizer - Playwright test suite
# Each test = one thing a real user would do, and what they SHOULD see per the spec (docs/SPEC.md).
# Tests marked xfail are KNOWN BUGS: they fail today on purpose and point to a bug report.
# strict=True means if the bug ever gets fixed, the run tells us to remove the xfail.
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

# Where the app lives (a local HTML file, so no internet needed)
APP = (Path(__file__).parent.parent / "apps" / "snowboard-sizer.html").as_uri()


def known_bug(bug_id, summary):
    """Marks a test that fails because of a filed bug."""
    return pytest.mark.xfail(reason=f"{bug_id}: {summary}", strict=True)


def fill_form(page: Page, height, weight, unit="kg", style="all", boot=""):
    """Types the user's info into the form and clicks the button."""
    page.goto(APP)                              # open the app
    page.fill("#h", str(height))                # height box
    page.fill("#w", str(weight))                # weight box
    page.select_option("#wu", unit)             # kg or lb dropdown
    page.select_option("#s", style)             # riding style dropdown
    page.fill("#b", str(boot))                  # boot size box
    page.click("#go")                           # "Find my board"


def expect_length(page: Page, cm):
    expect(page.locator("#out")).to_contain_text(f"{cm} cm")


def expect_error(page: Page):
    expect(page.locator("#out .err")).to_be_visible()


# ---------- Spec #1, #4: base length and rounding ----------

def test_normal_rider_gets_correct_length(page: Page):
    # 178 x 0.88 = 156.6 -> 157 cm. 75 kg = no adjustment.
    fill_form(page, height=178, weight=75)
    expect_length(page, 157)


def test_rounding_down(page: Page):
    # 175 x 0.88 = 154.0 -> 154 cm
    fill_form(page, height=175, weight=75)
    expect_length(page, 154)


# ---------- Spec #2: weight adjustment (boundaries at 55 and 90 kg) ----------

@pytest.mark.parametrize("weight, expected", [
    (95, 160),   # over 90 -> +3
    (90, 157),   # exactly 90 -> no change (boundary)
    (55, 157),   # exactly 55 -> no change (boundary)
    (50, 154),   # under 55 -> -3
])
def test_weight_adjustment(page: Page, weight, expected):
    fill_form(page, height=178, weight=weight)
    expect_length(page, expected)


# ---------- Spec #3: riding style ----------

def test_freestyle_is_2cm_shorter(page: Page):
    # 156.6 - 2 = 154.6 -> 155
    fill_form(page, height=178, weight=75, style="free")
    expect_length(page, 155)


@known_bug("BUG-002", "Powder adds +2 cm instead of +4 cm")
def test_powder_is_4cm_longer(page: Page):
    # 156.6 + 4 = 160.6 -> 161 (app shows 159)
    fill_form(page, height=178, weight=75, style="powder")
    expect_length(page, 161)


# ---------- Spec #5: pounds ----------

def test_pounds_far_from_boundary(page: Page):
    # 165 lb = 74.8 kg -> no adjustment -> 157
    fill_form(page, height=178, weight=165, unit="lb")
    expect_length(page, 157)


@known_bug("BUG-001", "lb converted by dividing by 2 instead of 2.2046")
def test_pounds_light_rider(page: Page):
    # 120 lb = 54.4 kg, under 55 -> 157 - 3 = 154 (app shows 157)
    fill_form(page, height=178, weight=120, unit="lb")
    expect_length(page, 154)


@known_bug("BUG-001", "lb converted by dividing by 2 instead of 2.2046")
def test_pounds_heavy_boundary(page: Page):
    # 190 lb = 86.2 kg, NOT over 90 -> 180 x 0.88 = 158.4 -> 158 (app shows 161)
    fill_form(page, height=180, weight=190, unit="lb")
    expect_length(page, 158)


# ---------- Spec #6, #7: valid ranges ----------

def test_min_height_allowed(page: Page):
    # 120 x 0.88 = 105.6 -> 106
    fill_form(page, height=120, weight=75)
    expect_length(page, 106)


@known_bug("BUG-003", "Max height 220 cm is rejected (off-by-one)")
def test_max_height_allowed(page: Page):
    # 220 x 0.88 = 193.6, 100 kg -> +3 = 196.6 -> 197
    fill_form(page, height=220, weight=100)
    expect_length(page, 197)


@pytest.mark.parametrize("height", [119, 221])
def test_height_out_of_range_rejected(page: Page, height):
    fill_form(page, height=height, weight=75)
    expect_error(page)


def test_weight_over_150_rejected(page: Page):
    fill_form(page, height=178, weight=151)
    expect_error(page)


# ---------- Spec #8: missing fields ----------

def test_empty_height_shows_error(page: Page):
    fill_form(page, height="", weight=75)
    expect_error(page)


@known_bug("BUG-005", "Empty weight gives a board size instead of an error")
def test_empty_weight_shows_error(page: Page):
    fill_form(page, height=178, weight="")
    expect_error(page)


# ---------- Spec #9: wide boards ----------

def test_boot_10_5_no_wide(page: Page):
    fill_form(page, height=180, weight=80, boot=10.5)
    expect(page.locator("#out")).not_to_contain_text("WIDE")


def test_boot_11_5_gets_wide(page: Page):
    fill_form(page, height=180, weight=80, boot=11.5)
    expect(page.locator("#out")).to_contain_text("WIDE")


@known_bug("BUG-004", "Boot size exactly 11 doesn't recommend a wide board")
def test_boot_11_gets_wide(page: Page):
    fill_form(page, height=180, weight=80, boot=11)
    expect(page.locator("#out")).to_contain_text("WIDE")
