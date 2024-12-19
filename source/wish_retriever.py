from collections.abc import Mapping, MutableMapping

import numpy as np
from pandas import DataFrame

from source.constants import (
    GENDER_COLUMN,
    GENDERS,
    NAME_COLUMN,
    PARTNER_COLUMN,
    SOCIAL_ANSWERS,
    SOCIAL_COLUMN,
    WISH_COLUMNS,
)


def _create_wishes(
    df: DataFrame,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    academic_wishes: dict[str, list[str]] = {}
    social_wishes: dict[str, list[str]] = {}

    for _, row in df.iterrows():
        name = row[NAME_COLUMN]
        friends = [
            row[wish] for wish in WISH_COLUMNS if isinstance(row[wish], str)
        ]

        if len(friends) != len(set(friends)):
            raise ValueError(
                f"{name} has duplicate entries in their wish list."
            )

        academic_wishes[name] = friends
        social_wishes[name] = friends.copy()
        partner = row[PARTNER_COLUMN]

        if isinstance(partner, str):
            social_wishes[name].insert(0, partner)

    return academic_wishes, social_wishes


def _fill_wishes(df: DataFrame, wishes: Mapping[str, list[str]]) -> None:
    genders: dict[str, str] = dict(zip(df[NAME_COLUMN], df[GENDER_COLUMN]))
    partners: dict[str, str] = dict(zip(df[NAME_COLUMN], df[PARTNER_COLUMN]))

    girls_names: list[str] = sorted(
        df.loc[df[GENDER_COLUMN] == GENDERS[0], NAME_COLUMN].tolist()
    )
    boys_names: list[str] = sorted(
        df.loc[df[GENDER_COLUMN] == GENDERS[1], NAME_COLUMN].tolist()
    )

    for person in wishes:
        girls_names_2 = girls_names.copy()
        boys_names_2 = boys_names.copy()

        rng = np.random.default_rng(abs(hash(person)))
        rng.shuffle(girls_names_2)
        rng.shuffle(boys_names_2)

        primary_names, secondary_names = (
            (girls_names_2, boys_names_2)
            if genders[person] == GENDERS[0]
            else (boys_names_2, girls_names_2)
        )

        wishes[person].extend(
            name
            for name in primary_names
            if name not in wishes[person] and name != person
        )
        wishes[person].extend(
            name for name in secondary_names if name != partners[person]
        )


def _remove_asocialites(
    df: DataFrame, wishes: MutableMapping[str, list[str]], verbose: bool = True
) -> None:
    for _, row in df.iterrows():
        if row[SOCIAL_COLUMN] == SOCIAL_ANSWERS[0]:
            continue

        name = row[NAME_COLUMN]
        wishes.pop(name, None)

        if verbose:
            print(f"Removed {name!r} from wishes.")

        for person in wishes:
            if name in wishes[person]:
                wishes[person].remove(name)


def get_wishes(
    df: DataFrame,
) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    academic_wishes, social_wishes = _create_wishes(df)

    initial_wishes = social_wishes.copy()
    _remove_asocialites(df, initial_wishes, verbose=False)

    _fill_wishes(df, social_wishes)
    _remove_asocialites(df, social_wishes)

    return academic_wishes, initial_wishes, social_wishes
