def lists_contain_same_objects(expected: list[object], actual: list[object]) -> bool:
    unmatched_entries = [obj for obj in expected if obj not in actual]

    if not unmatched_entries:
        return True

    for u in unmatched_entries:
        print(f"---Missing person:\n{u}")

    return False
