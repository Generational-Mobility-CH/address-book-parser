ALLOWED_SPECIAL_CHARS = (",", ".", "-", "—", " ", "(", ")", "ß")
GERMAN_UMLAUTE = {"ä": "ae", "ö": "oe", "ü": "ue"}
GERMAN_VOWELS = set("aeiouäöü")
KEYWORDS_NAMES_SEPARATOR = (
    "dit",
    " dr.",
    " dr ",
    " dr med  dr. phil.",
    "frau",
    "gent.",
    "prof.",
    "wittwe",
    "ww.",
    "wwe",
)
KEYWORDS_STREET_NAME = ("gass", "gaß", "platz", "allee")
PLACEHOLDERS_LAST_NAME = ("—", "-")
PLACEHOLDER_GESCHIEDEN = ("gesc.", "gesch.")
PLACEHOLDER_WIDOW = "ww"
TAG_NONE_FOUND = "<KEINE ANGABE GEFUNDEN>"
TAG_NO_JOB = "<KEINEN JOB GEFUNDEN>"
UNALLOWED_STRINGS = (
    "$\\S$ text ",
    "text ",
    " text",
    " f ",
    "fractext",
    " fractext",
    "fractext ",
    "fracmathfrakfmathfrakf",
    "fracmath",
    " fracmath",
    "fracmath ",
    "fracmathfrakf",
    "mathfrak",
    "frac",
    " frac",
    "frac ",
    "frakf",
    " frakf",
    "frakf ",
    "bullet",
    "therefore",
    "otimes",
    "oplus",
    "odot",
    "|",
    "½",
    "circ",
    "Dagger",
    "dagger",
    "Φ",
    "φ",
    "ψ",
    "α",
    "@",
    "diamond",
    "()",
)
UNALLOWED_AT_START_OF_STRING = ("of ", "ž", "Š", "ß", ")")
SPECIAL_NAME_RANGE_LETTERS = set("ij")
COMPANY_KEYWORDS = (
    "aktiengesel",
    "aufbewahrung",
    "börse",
    "compagnie",
    "company",
    "conférence",
    "genossenschaft",
    "geschäft",
    "handel",
    "konsulat",
    "lager",
    "maschinen",
    "mechan",
    "société",
    "textil",
    "verein",
    "versicherung",
    "werkstatt",
)
