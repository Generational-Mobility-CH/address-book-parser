ALLOWED_SPECIAL_CHARS = (",", ".", "-", "—", " ", "(", ")", "ß")
GERMAN_UMLAUTE = {"ä": "ae", "ö": "oe", "ü": "ue"}
GERMAN_VOWELS = set("aeiouäöü")
KEYWORDS_NAMES_SEPARATOR = (
    "wittwe",
    "ww.",
    "wwe",
    "prof.",
    " dr. phil.",
    " dr.",
    "frau",
    "gent.",
)
SPECIAL_LAST_NAMES_MAP = {
    " van der ": "VanDer",
    " von der ": "VonDer",
    " de la roche ": "DeLaRoche",
    " la roche ": "LaRoche",
    " de la ": "DeLa",
    " de ": "De",
    " dal ": "Dal",
    " del ": "Del",
    " della ": "Della",
    " des ": "Des",
    " la ": "La",
    " le ": "Le",
    " van ": "Van",
    " vom ": "Vom",
    " von ": "Von",
    " zum ": "Zum",
}
KEYWORDS_STREET_NAME = ("gass", "gaß", "platz", "allee")
PLACEHOLDERS_SURNAME = ("—", "-")
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
    "konsulat",
    "aktiengesel",
    "verein",
    "conférence",
    "textil",
    "handel",
    "geschäft",
    "börse",
    "mechan",
    "werkstatt",
)
