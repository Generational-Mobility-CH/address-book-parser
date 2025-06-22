from modules.models.person import Person


def transform(data: list[Person]) -> list[Person]:
    return [person.standardize_attributes() for person in data]
