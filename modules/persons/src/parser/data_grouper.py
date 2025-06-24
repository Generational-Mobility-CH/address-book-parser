def group_data(text: list[str]) -> list[list[str]]:
    """
    Separate each string into substrings containing information bits.
    In a later step these information bits will be checked and parsed into the relevant attributes of a person:
        - name
        - address
        - job
    """
    result = []

    for line in text:
        content = line.split(",")
        content = [item for item in content if item != ""]

        if len(content) in (2, 3):
            result.append(content)

    return result
