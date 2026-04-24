"""
Prompts for dots.ocr-1.5 transcription of historical address book pages.

P10V_MINIMAL_PLUS: Best-performing prompt from benchmark v6 (1940-1950).
Achieves 95.85% prefix accuracy, 98.61% text accuracy across 40 GT pages.
"""

P10V_MINIMAL_PLUS = (
    "Transcribe this German address book page. Number each entry. "
    "Join wrapped lines.\n"
    "Copy leading symbols exactly: \u25cf \u2021 \u2014 -\n"
    "\u25cf then \u2021 then \u2014 then -. Include \u2021 only when printed. "
    "The first entry may or may not have \u2021.\n"
    "\u2014 alone and \u2014 - are different prefixes: "
    "output both marks only when both are visible.\n\n"
    "1. \u25cf\u2021\u2014 -Name \u2026\n"
    "2. \u2021\u2014Name \u2026\n"
    "3. \u2014 -Name \u2026\n"
    "4. \u2014Name \u2026\n"
    "5. Name \u2026\n\n"
    "Numbered entries only."
)

P10V_NO_FIRSTDAGGER_RERUN = (
    "Transcribe this German address book page. Number each entry.\n"
    "If an entry wraps across printed lines, join it into one numbered line.\n"
    "Preserve all leading symbols: \u25cf (bullet), \u2021 (cross/dagger), "
    "\u2014 (em-dash), - (hyphen).\n"
    "Symbols appear in order: \u25cf then \u2021 then \u2014 then -.\n"
    "Output \u2014 - only when both marks are visible; "
    "\u2014 alone otherwise.\n"
    "Include \u2021 when present; omit it when absent. "
    "The first entry does not always have \u2021.\n\n"
    "Format:\n"
    "1. \u2021Name, occupation, address\n"
    "2. \u2014 -Name, occupation, address\n"
    "3. \u25cf\u2021\u2014 -Name, occupation, address\n"
    "4. Name, occupation, address\n\n"
    "Output all entries numbered. No other commentary."
)

ACTIVE_PROMPT = P10V_NO_FIRSTDAGGER_RERUN
