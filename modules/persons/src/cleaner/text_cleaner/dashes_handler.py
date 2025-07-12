def clean_up_dashes(line: str) -> str:
    line = line.replace("—", "-")
    line = line.replace(" - ", "-")
    line = line.replace("- ", "-")
    line = line.replace(" -", "-")

    result = ""
    previous_was_dash = False

    for char in line:
        if char == "-":
            if previous_was_dash:
                continue
            previous_was_dash = True
        else:
            previous_was_dash = False

        result += char

    return result
