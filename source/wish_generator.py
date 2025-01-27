import numpy as np
import pandas as pd
from numpy.random import Generator
from pandas import DataFrame

from source.constants import (
    GENDERS,
    GLOBAL_COLUMNS,
    PARTNER_COLUMN,
    SOCIAL_ANSWERS,
    SOCIAL_COLUMN,
    UNUSED_COLUMNS,
    WISH_COLUMNS,
    WISHES_FILE,
)


def _generate_rows(rng: Generator) -> list[list[str | None]]:
    rows: list[list[str | None]] = []
    all_names = (GIRLS_NAMES, BOYS_NAMES)

    for gender, names in zip(GENDERS, all_names):
        for name in names:
            other_names = names.copy()
            other_names.remove(name)

            row: list[str | None] = [name]
            row.append(SOCIAL_ANSWERS[0])
            row.append(gender)

            max_wishes = len(WISH_COLUMNS)
            n = rng.integers(1, max_wishes + 1)
            row.extend(
                str(wish) for wish in rng.choice(other_names, n, replace=False)
            )
            row.extend([None] * (max_wishes - n))

            row.append(None)  # Partner
            rows.append(row)

    return rows


def _assign_sociality(rng: Generator, rows: list[list[str | None]]) -> None:
    pairs = 5
    asocials = 5

    girls_end = len(GIRLS_NAMES)
    random_girls_indices = rng.choice(girls_end, pairs, replace=False)
    random_boys_indices = rng.choice(
        range(girls_end, len(rows)), pairs + asocials, replace=False
    )
    random_girls = [rows[i] for i in random_girls_indices]
    random_boys = [rows[i] for i in random_boys_indices]

    partner_idx = GLOBAL_COLUMNS.index(PARTNER_COLUMN)
    social_idx = GLOBAL_COLUMNS.index(SOCIAL_COLUMN)

    for boy, girl in zip(random_boys, random_girls, strict=False):
        boy[partner_idx] = girl[0]
        girl[partner_idx] = boy[0]
    for boy in random_boys[pairs:]:
        boy[social_idx] = SOCIAL_ANSWERS[1]


def create_dummy_wishes(seed: int = 69_420) -> DataFrame:
    rng = np.random.default_rng(seed)

    rows = _generate_rows(rng)
    _assign_sociality(rng, rows)
    df = DataFrame(rows, columns=GLOBAL_COLUMNS)

    df.to_csv(WISHES_FILE, index=False)
    print(f"Wrote {len(df)} wishes to {WISHES_FILE!r}.")
    return df


def _fix_columns(df: DataFrame) -> DataFrame:
    first_columns = WISH_COLUMNS + [PARTNER_COLUMN]
    second_columns = [f"{column}." for column in first_columns]

    for first_column, second_column in zip(first_columns, second_columns):
        if second_column not in df.columns:
            continue

        df[first_column] = df[first_column].combine_first(df[second_column])

    df.drop(columns=second_columns, errors="ignore", inplace=True)
    df.drop(columns=UNUSED_COLUMNS, errors="ignore", inplace=True)
    return df


def read_wishes(fix: bool = True) -> DataFrame:
    df = pd.read_csv(WISHES_FILE)

    if fix:
        df = _fix_columns(df)
        df.to_csv(WISHES_FILE, index=False)

    return df[GLOBAL_COLUMNS]


GIRLS_NAMES = [
    "Anna",
    "Antonie",
    "Ingeborg",
    "Julie",
    "Kaja",
    "Karoline",
    "Madelen",
    "Maja",
    "Maren",
    "Marthe",
    "Martine",
    "Nora",
    "Solveig",
    "Vanessa",
    "Vilde",
]
BOYS_NAMES = [
    "Aksel",
    "Aleksander",
    "Altay",
    "Anders",
    "Andreas D.",
    "Andreas I.",
    "Andreas B.",
    "Axel",
    "Christoffer",
    "Edvin",
    "Eirik O.",
    "Eirik S.",
    "Eivind",
    "Emrik",
    "Fredrik",
    "Gjermund",
    "Hamze",
    "Heine",
    "Jakob",
    "Jan",
    "Jo",
    "Kasper",
    "Kristoffer",
    "Magnus O.",
    "Magnus J.",
    "Manav",
    "Martin",
    "Morten",
    "Nils",
    "Ole",
    "Per",
    "Petter",
    "Robin",
    "Sindre",
    "Sondre",
    "Torbjørn",
    "Truls",
    "Viktor",
]
