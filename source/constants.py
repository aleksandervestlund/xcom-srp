from typing import TypeAlias


WISHES_FILE = "wishes.csv"
MATCHING_FILE = "matching.json"

NAME_COLUMN = "Hva er ditt navn?"
SOCIAL_COLUMN = "Skal du delta på sosial del?"
GENDER_COLUMN = "Hvilket kjønn er du?"
WISH_COLUMNS = ["Førstevalg", "Andrevalg", "Tredjevalg"]
PARTNER_COLUMN = "Sosialt ønske"

GLOBAL_COLUMNS = [
    NAME_COLUMN,
    SOCIAL_COLUMN,
    GENDER_COLUMN,
    *WISH_COLUMNS,
    PARTNER_COLUMN,
]

SOCIAL_ANSWERS = ("Ja", "Nei")
GENDERS = ("Jente", "Gutt")

Wishes: TypeAlias = dict[str, list[str]]
Matching: TypeAlias = dict[str, str]
