from modules.panel_data.src.models.new_person import NewPerson


def standardize_first_names(persons: list[NewPerson]) -> list[NewPerson]:
    # TODO
    return persons


def standardize_job(persons: list[NewPerson]) -> list[NewPerson]:
    # TODO
    return persons


def standardize_information(persons: list[NewPerson]) -> list[NewPerson]:
    persons = standardize_first_names(persons)
    persons = standardize_job(persons)

    return persons
