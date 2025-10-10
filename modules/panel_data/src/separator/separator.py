from modules.panel_data.src.models.new_person import NewPerson
from modules.panel_data.src.separator.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from modules.panel_data.src.separator.partner_last_name_separator import (
    separate_partner_last_name,
)
from modules.persons_data_processor.src.models.person.person import Person


def separate_information(persons: list[Person]) -> list[NewPerson]:
    persons = separate_last_and_first_names(persons)
    persons = separate_partner_last_name(persons)

    return persons
