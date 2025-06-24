def ends_with_number(line: str) -> bool:
    """
    Heuristik: Adresse über 2 Zeilen, wenn Zeile mit Zahl endet.
    Bsp.: - Struchen Emanuel, Schuhmacherstr., 93
    Elsässerstr.
    """
    # TODO: can this be done through built-in python functions?
    return bool(line) and line[-1].isnumeric()


def has_line_break(line: str) -> bool:
    return bool(line) and line[-1] == "-"


def merge_line_break(current_line: str, next_line: str) -> str:
    if next_line.lower().startswith("und"):
        next_line = next_line.replace("und", " und")

    line = current_line + " " + next_line
    return line.replace("- ", "")
