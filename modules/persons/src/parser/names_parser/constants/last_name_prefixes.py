# Order: From the longest prefixes (e.g. multi-word prefixes) to the shortest
# Reason: To avoid wrong matches. E.g. matching only 'de' in a name with 'de la'
LAST_NAME_PREFIXES_MAP = {
    " aus der ": "AusDer",
    " van der ": "VanDer",
    " van den ": "VanDen",
    " von der ": "VonDer",
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
    " v. ": "Von",
}
SPECIAL_LAST_NAMES_MAP = {
    " de la roche ": "DeLaRoche",
    " von der mühl ": "VonDerMühl",
    " von der schmitt ": "VonDerSchmitt",
}
