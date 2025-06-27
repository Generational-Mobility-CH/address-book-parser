# TODO: use set() instead of list for faster look-up
ALLOWED_SPECIAL_CHARS = [",", ".", "-", "—", " ", "(", ")", "ß"]
KEYWORDS_NAMES_SEPARATOR = ["wittwe", "ww.", "wwe", "prof.", " dr.", "frau"]
SPECIAL_LAST_NAMES_MAP = {
    " van der ": "VanDer",
    " von der ": "VonDer",
    " de la ": "DeLa",
    " de ": "De",
    " dal ": "Dal",
    " del ": "Del",
    " della ": "Della",
    " des ": "Des",
    # " la ": "La",  # TODO: implement handling later (la roche, de la roche...)
    " le ": "Le",
    " van ": "Van",
    " vom ": "Vom",
    " von ": "Von",
    " zum ": "Zum",
}
KEYWORDS_STREET_NAME = ["gass", "gaß", "platz", "allee"]
PLACEHOLDERS_SURNAME = ["—", "-"]
PLACEHOLDER_WIDOW = "ww"
TAG_NONE_FOUND = "<KEINE ANGABE GEFUNDEN>"
TAG_NO_JOB = "<KEINEN JOB GEFUNDEN>"
UNALLOWED_STRINGS = [
    "fractext",
    "f text",
    "f text f",
    "text",
    "therefore",
    "otimes",
    "oplus",
    "odot",
    "|",
    "½",
    "bullet",
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
]
UNALLOWED_AT_START_OF_STRING = ["of ", "ž", "Š", "ß", ")"]
UNALLOWED_WORDS = ["fracmath", "bullet"]
