"""
Evaluation functions for OCR benchmark against ground truth.

Handles parsing model output, extracting prefixes, matching against
ground truth entries, and computing accuracy metrics.

Ported from For_testing_general/src/evaluation.py.
"""
import json
import re
from difflib import SequenceMatcher


def parse_output_lines(raw: str) -> list[str]:
    """Parse full transcription output into list of entry lines."""
    lines = []
    raw_lines = raw.splitlines()
    i = 0
    while i < len(raw_lines):
        stripped = raw_lines[i].strip()
        if not stripped or stripped.startswith("```") or stripped == "---":
            i += 1
            continue
        if stripped.startswith("SYMBOLS:"):
            sym_part = stripped[len("SYMBOLS:") :].strip()
            i += 1
            while i < len(raw_lines):
                next_line = raw_lines[i].strip()
                if next_line.startswith("TEXT:"):
                    txt_part = next_line[len("TEXT:") :].strip()
                    combined = (
                        f"{sym_part} {txt_part}".strip() if sym_part else txt_part
                    )
                    lines.append(combined)
                    i += 1
                    break
                i += 1
            continue
        # Strip leading numbering (1. or a))
        stripped = re.sub(r"^\d+\.\s+", "", stripped)
        stripped = re.sub(r"^[a-z]+\)\s+", "", stripped)
        stripped = re.sub(r"<sym>(.*?)</sym>\s*", r"\1", stripped)
        stripped = re.sub(
            r"^[\[\u25cf\u2021\u2014 -]*\]\s*",
            lambda m: m.group(0).strip("[] ") + " ",
            stripped,
        ).strip()
        if stripped.startswith("{") and '"txt"' in stripped:
            try:
                obj = json.loads(stripped)
                pfx = obj.get("pfx", "")
                txt = obj.get("txt", "")
                combined = f"{pfx} {txt}".strip() if pfx else txt
                lines.append(combined)
                i += 1
                continue
            except (json.JSONDecodeError, ValueError):
                pass
        if stripped:
            lines.append(stripped)
        i += 1
    return lines


def extract_prefix(line: str) -> tuple[str, str]:
    """Extract prefix symbols and text from a transcription line."""
    pipe_match = re.match(
        r"^([\u25cf\u2021\u00b7\u2014\u2013 -]*?)\s*\|\s*(.*)", line
    )
    if pipe_match:
        pfx = pipe_match.group(1).strip()
        txt = pipe_match.group(2).strip()
        pfx = re.sub(r"\s+", " ", pfx)
        return pfx, txt
    m = re.match(
        r"^([\u25cf\u2021\u00b7]*\s*(?:[\u2014\u2013]\s*-?\s*)?)\s*(.*)", line
    )
    if m and m.group(1).strip():
        pfx = m.group(1).strip()
        txt = m.group(2).strip()
        pfx = re.sub(r"\s+", " ", pfx)
        return pfx, txt
    return "", line.strip()


def normalize_dash_prefix(pfx: str) -> str:
    """Normalize prefix to just the dash component for comparison."""
    dash_only = re.sub(r"[\u25cf\u2021\u00b7]", "", pfx).strip()
    dash_only = re.sub(r"\u2014\s*-", "\u2014 -", dash_only)
    dash_only = dash_only.replace("\u2013", "\u2014")
    return dash_only


def text_similarity(a: str, b: str) -> float:
    """Character-level similarity between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_best_match(
    gt_txt: str, output_lines: list[str], used: set[int]
) -> tuple[int, float]:
    """Find the best matching output line for a ground truth entry."""
    best_score = 0.0
    best_idx = -1
    for i, line in enumerate(output_lines):
        if i in used:
            continue
        _, line_txt = extract_prefix(line)
        score = text_similarity(gt_txt, line_txt)
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx, best_score


def compute_text_diff(gt: str, model: str) -> str:
    """Compute a human-readable diff between GT and model text."""
    if gt == model:
        return ""
    sm = SequenceMatcher(None, gt, model)
    parts = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            parts.append(gt[i1:i2])
        elif op == "replace":
            parts.append(f"[{gt[i1:i2]}\u2192{model[j1:j2]}]")
        elif op == "delete":
            parts.append(f"[-{gt[i1:i2]}]")
        elif op == "insert":
            parts.append(f"[+{model[j1:j2]}]")
    return "".join(parts)


def evaluate(
    raw: str, gt: list[dict], postprocess_fn=None
) -> tuple[list[dict], dict]:
    """Evaluate full-transcription output against ground truth.

    Args:
        raw: Raw model output (numbered format, before conversion)
        gt: List of {"pfx": str, "txt": str} ground truth entries
        postprocess_fn: Optional function to apply to raw before parsing

    Returns:
        (entries_list, summary_dict) where each entry has pfx_score,
        txt_score, dash_match, found, etc.
    """
    if postprocess_fn:
        raw = postprocess_fn(raw)
    output_lines = parse_output_lines(raw)
    used: set[int] = set()
    entries = []

    for gt_entry in gt:
        gt_pfx = gt_entry["pfx"]
        gt_txt = gt_entry["txt"]
        gt_dash = normalize_dash_prefix(gt_pfx)

        idx, txt_score = find_best_match(gt_txt, output_lines, used)

        if idx >= 0 and txt_score > 0.4:
            used.add(idx)
            model_pfx, model_txt = extract_prefix(output_lines[idx])
            model_dash = normalize_dash_prefix(model_pfx)
            dash_match = gt_dash == model_dash
            pfx_score = (
                text_similarity(gt_pfx, model_pfx)
                if gt_pfx or model_pfx
                else 1.0
            )

            entries.append(
                {
                    "gt_pfx": gt_pfx,
                    "gt_txt": gt_txt,
                    "model_pfx": model_pfx,
                    "model_txt": model_txt,
                    "txt_score": txt_score,
                    "pfx_score": pfx_score,
                    "dash_match": dash_match,
                    "found": True,
                }
            )
        else:
            entries.append(
                {
                    "gt_pfx": gt_pfx,
                    "gt_txt": gt_txt,
                    "model_pfx": "",
                    "model_txt": "",
                    "txt_score": 0.0,
                    "pfx_score": 0.0,
                    "dash_match": False,
                    "found": False,
                }
            )

    n = len(entries)
    found = sum(1 for e in entries if e["found"])
    pfx_mean = sum(e["pfx_score"] for e in entries) / n if n else 0
    txt_mean = sum(e["txt_score"] for e in entries) / n if n else 0
    dash_ok = sum(1 for e in entries if e["dash_match"])

    hyph = [e for e in entries if "\u2014 -" in e["gt_pfx"]]
    hyph_ok = sum(1 for e in hyph if e["dash_match"])
    no_hyph = [
        e
        for e in entries
        if e["gt_pfx"].endswith("\u2014")
        and "-" not in e["gt_pfx"].replace("\u2014", "")
    ]
    no_hyph_ok = sum(1 for e in no_hyph if e["dash_match"])

    summary = {
        "pfx_mean": pfx_mean,
        "txt_mean": txt_mean,
        "found": found,
        "total": n,
        "dash_ok": dash_ok,
        "hyph_ok": hyph_ok,
        "hyph_total": len(hyph),
        "no_hyph_ok": no_hyph_ok,
        "no_hyph_total": len(no_hyph),
    }
    return entries, summary
