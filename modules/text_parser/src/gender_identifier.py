from dataclasses import dataclass

from modules.text_parser.src.constants.gender_descriptors import (
    GENDER_FEMALE,
    GENDER_MALE,
    GENDER_UNKNOWN,
)
from modules.text_parser.src.constants.female_names_not_ending_in_a import (
    FEMALE_NAMES_NOT_ENDING_IN_A,
)
from modules.text_parser.src.constants.male_names_ending_in_a import (
    MALE_NAMES_ENDING_IN_A,
)
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_standardizer.src.constants.name_abbreviations import (
    FIRST_NAME_ABBREVIATIONS_MAP_MALE,
)


_GENDER_CONFIDENCE_HIGH = "HIGH"
_GENDER_CONFIDENCE_MIDDLE = "MIDDLE"
_GENDER_CONFIDENCE_LOW = "LOW"


@dataclass
class GenderFactor:
    name: str
    confidence: str
    gender: str


def found_female_keyword(data: str) -> bool:
    data = data.lower().strip()
    return data.startswith(
        "wwe. "
    )  # TODO: check if abbreviation is already normalized? Ww. wwe.??


def found_female_first_name(data: str) -> bool:
    data = data.strip().lower()
    return (
        data.endswith("a") and data not in MALE_NAMES_ENDING_IN_A
    ) or data in FEMALE_NAMES_NOT_ENDING_IN_A


def found_female_job(data: str) -> bool:
    return data.strip().endswith("in")


def found_male_first_name(data: str) -> bool:
    data = data.strip().lower()
    return (
        (data in MALE_NAMES_ENDING_IN_A)
        or data in FIRST_NAME_ABBREVIATIONS_MAP_MALE.keys()
        or data in FIRST_NAME_ABBREVIATIONS_MAP_MALE
    )


def found_male_job(data: str) -> bool:
    return data.strip().endswith("er")


def _infer_gender(factors: list[GenderFactor]) -> str:
    if not factors:
        # default value is 'male', since men are overrepresented in data
        return GENDER_MALE

    counts = {GENDER_FEMALE: 0, GENDER_MALE: 0}
    confidence_values = {
        _GENDER_CONFIDENCE_HIGH: 3,
        _GENDER_CONFIDENCE_MIDDLE: 2,
        _GENDER_CONFIDENCE_LOW: 1,
    }

    for f in factors:
        counts[f.gender] += confidence_values.get(f.confidence, 0)

    return (
        GENDER_FEMALE
        if counts[GENDER_FEMALE] > counts[GENDER_MALE]
        else GENDER_MALE
        if counts[GENDER_MALE] > counts[GENDER_FEMALE]
        else GENDER_UNKNOWN
    )


def _persist_gender_factors(factors: list[GenderFactor]) -> str:
    if not factors:
        return f"'{GENDER_MALE}' from NO_FEMALE_FACTORS_FOUND weight={_GENDER_CONFIDENCE_LOW}"

    return "; ".join(
        f"'{f.gender}' from {f.name} weight={f.confidence}" for f in factors
    )


def identify_gender(persons_collection: list[PanelDataEntry]) -> list[PanelDataEntry]:
    for person in persons_collection:
        gender_factors: list[GenderFactor] = []

        if found_female_keyword(person.first_names):
            gender_factors.append(
                GenderFactor(
                    name="KEYWORD",
                    confidence=_GENDER_CONFIDENCE_HIGH,
                    gender=GENDER_FEMALE,
                )
            )

        if found_female_first_name(person.first_names):
            gender_factors.append(
                GenderFactor(
                    name="FIRST_NAME",
                    confidence=_GENDER_CONFIDENCE_MIDDLE,
                    gender=GENDER_FEMALE,
                )
            )

        if found_female_job(person.job):
            gender_factors.append(
                GenderFactor(
                    name="JOB", confidence=_GENDER_CONFIDENCE_LOW, gender=GENDER_FEMALE
                )
            )

        if found_male_first_name(person.first_names):
            gender_factors.append(
                GenderFactor(
                    name="FIRST_NAME",
                    confidence=_GENDER_CONFIDENCE_MIDDLE,
                    gender=GENDER_MALE,
                )
            )

        if found_male_job(person.job):
            gender_factors.append(
                GenderFactor(
                    name="JOB", confidence=_GENDER_CONFIDENCE_LOW, gender=GENDER_MALE
                )
            )

        person.gender = _infer_gender(gender_factors)
        person.gender_confidence = _persist_gender_factors(gender_factors)

    return persons_collection
