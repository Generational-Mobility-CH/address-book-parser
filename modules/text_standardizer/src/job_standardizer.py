from libs.regex.src.substitute_with_map import substitute_with_map
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_standardizer.src.constants.job_substitutions import (
    JOBS_SUBSTITUTION_MAP,
)


ABBREVIATED_JOB_PATTERN = "{PLACEHOLDER}"


def standardize_job(person: PanelDataEntry) -> PanelDataEntry:
    job = person.job.lower()

    if "." in job:
        # edge case: when using 'substitute_with_map()' we would strip " u. " -> "u.", so a special case was added for this abbreviation.
        if " u. " in job:
            job = job.replace(" u. ", " und ")

        cleaned_job = substitute_with_map(
            job, JOBS_SUBSTITUTION_MAP, ABBREVIATED_JOB_PATTERN
        )
        person.job = cleaned_job

    return person
