"""
Postprocessing for dots.ocr-1.5 model output.
Fixes known character substitutions before evaluation.
"""
import re


def postprocess_raw(raw: str) -> str:
    """Fix known character substitutions in model output before evaluation.

    Known issues found via hex analysis of all s2v_*.txt outputs:
    - } (U+007D) and { (U+007B) used instead of \u2021 (U+2021)
    - \u25ce (U+25CE bullseye) used instead of \u25cf (U+25CF)
    - \u00a4 (U+00A4 currency sign) used instead of \u2021
    - Spurious space between \u2021 and \u2014 (e.g. '\u2021 \u2014' -> '\u2021\u2014')
    - Hyphen-minus used instead of em-dash after \u2021 (e.g. '\u2021-' -> '\u2021\u2014')
    """
    lines = raw.splitlines()
    result = []
    for line in lines:
        # Strip line number to work on content, then re-add
        m = re.match(r"^(\d+\.\s*)(.*)", line)
        if m:
            num_part, content = m.group(1), m.group(2)
        else:
            num_part, content = "", line

        # 1. } -> \u2021 and { -> \u2021 (model substitutes curly braces for dagger)
        content = content.replace("}", "\u2021").replace("{", "\u2021")

        # 2. \u25ce -> \u25cf (bullseye substitution for bullet)
        content = content.replace("\u25ce", "\u25cf")

        # 3. \u00a4 -> \u2021 (currency sign substitution)
        content = content.replace("\u00a4", "\u2021")

        # 3b. Collapse doubled em-dashes: \u2014 \u2014 -> \u2014
        content = re.sub(r"\u2014(\s*\u2014)+", "\u2014", content)

        # 4. Normalize spacing: \u2021 \u2014 -> \u2021\u2014
        content = re.sub(r"\u2021\s+\u2014", "\u2021\u2014", content)

        # 5. \u25cf \u2021 -> \u25cf\u2021
        content = re.sub(r"\u25cf\s+\u2021", "\u25cf\u2021", content)

        # 6. Hyphen-minus after \u2021 where em-dash expected:
        #    \u2021- - -> \u2021\u2014 -  (first hyphen is em-dash, second is partner)
        content = re.sub(r"\u2021\s*-(\s*-)", "\u2021\u2014\\1", content)
        #    \u2021- followed by capital letter or ( -> \u2021\u2014
        content = re.sub(
            r"\u2021\s*-(?=[A-Z\u00c4\u00d6\u00dc(])", "\u2021\u2014", content
        )

        # 7. Normalize spacing: \u2021\u2014 - with extra spaces -> \u2021\u2014 -
        content = re.sub(r"\u2021\u2014\s+-", "\u2021\u2014 -", content)

        # 8. Same for \u25cf prefix combinations: \u25cf\u2021 \u2014 -> \u25cf\u2021\u2014
        content = re.sub(r"\u25cf\u2021\s+\u2014", "\u25cf\u2021\u2014", content)

        result.append(num_part + content)
    return "\n".join(result)
