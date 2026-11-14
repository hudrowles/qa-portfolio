# QA-482 · Test the Board Sizer v2.3 before release

**Assigned to:** you    **Priority:** High    **Due:** end of day

## What changed
The dev team rebuilt the snowboard size calculator (`snowboard-sizer.html`). Before it goes live,
QA needs to confirm it matches the product spec below. Find anything that doesn't.

## Product spec (how it's SUPPOSED to work)
1. Base length = height (cm) x 0.88
2. Weight adjustment: over 90 kg = +3 cm, under 55 kg = -3 cm, otherwise no change
3. Style adjustment: Freestyle = -2 cm, Powder = +4 cm, All-mountain = no change
4. Final length is rounded to the nearest whole cm
5. Weight can be entered in kg or lb (1 kg = 2.2046 lb)
6. Valid height: 120 to 220 cm, **inclusive** (120 and 220 are both allowed)
7. Valid weight: 30 to 150 kg, inclusive
8. Any missing or invalid field must show a clear error message, never a broken result
9. Boot size **11 or bigger** = recommend a WIDE board

## Your deliverables
- [ ] Write a short test plan: a list of the checks you'll run (aim for 10-15)
- [ ] Run every check, and work out the expected answer with a calculator first
- [ ] File one bug report per bug you find (use BUG_TEMPLATE.md)
- [ ] Post a one-line summary: "Tested X cases, found Y bugs, release is / isn't ready"
