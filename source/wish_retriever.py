import hashlib
from collections.abc import Iterable, Mapping, MutableMapping
from copy import deepcopy

import numpy as np
from networkx import Graph, single_source_shortest_path_length
from pandas import DataFrame

from source.constants import (
    GENDER_COLUMN,
    GENDERS,
    NAME_COLUMN,
    PARTNER_COLUMN,
    SOCIAL_ANSWERS,
    SOCIAL_COLUMN,
    WISH_COLUMNS,
    Wishes,
)
from source.graphs import add_wish_edge


def deterministic_seed(value: str) -> int:
    """Create a deterministic seed from a string, since Python's
    built-in `hash` is not deterministic across sessions.
    """
    # sha256 is arbitrarily chosen. Could be any hash function
    return int(hashlib.sha3_512(value.encode()).hexdigest(), 16) % 2**32


def _create_wishes(df: DataFrame) -> tuple[Wishes, Wishes]:
    academic_wishes: Wishes = {}
    social_wishes: Wishes = {}

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


def _shuffle_names(
    genders: Mapping[str, str],
    girls_names: list[str],
    boys_names: list[str],
    person: str,
) -> tuple[list[str], list[str]]:
    girls_names_2 = girls_names.copy()
    boys_names_2 = boys_names.copy()

    rng = np.random.default_rng(deterministic_seed(person))
    rng.shuffle(girls_names_2)
    rng.shuffle(boys_names_2)

    primary_names, secondary_names = (
        (girls_names_2, boys_names_2)
        if genders[person] == GENDERS[0]
        else (boys_names_2, girls_names_2)
    )

    return primary_names, secondary_names


def _compose_graphs(
    academic_wishes: Wishes, social_wishes: Wishes
) -> tuple[Graph, Graph]:
    academic_graph: Graph = Graph()
    social_graph: Graph = Graph()
    number_of_wishes = len(WISH_COLUMNS)

    for i in range(number_of_wishes):
        add_wish_edge(academic_wishes, i, academic_graph)
        add_wish_edge(social_wishes, i, social_graph)

    add_wish_edge(social_wishes, number_of_wishes + 1, social_graph)
    return academic_graph, social_graph


def _fill_wishes(
    df: DataFrame, academic_wishes: Wishes, social_wishes: Wishes
) -> None:
    academic_wishes = deepcopy(academic_wishes)
    _remove_asocialites(df, academic_wishes)

    genders: dict[str, str] = dict(zip(df[NAME_COLUMN], df[GENDER_COLUMN]))
    socialities: dict[str, str] = dict(zip(df[NAME_COLUMN], df[SOCIAL_COLUMN]))
    girls_names = sorted(
        name
        for name in genders
        if genders[name] == GENDERS[0]
        and socialities[name] == SOCIAL_ANSWERS[0]
    )
    boys_names = sorted(
        name
        for name in genders
        if genders[name] == GENDERS[1]
        and socialities[name] == SOCIAL_ANSWERS[0]
    )

    academic_graph, social_graph = _compose_graphs(
        academic_wishes, social_wishes
    )

    for person in social_wishes:
        gender = genders[person]

        # Fill in closest same gender friends
        path_lengths = single_source_shortest_path_length(
            academic_graph, person
        )
        sorted_names = sorted(path_lengths, key=lambda x: (path_lengths[x], x))
        social_wishes[person].extend(
            name
            for name in sorted_names
            if name not in social_wishes[person] and name != person
        )

        # Fill in close same gender friends
        path_lengths = single_source_shortest_path_length(social_graph, person)
        sorted_names = sorted(path_lengths, key=lambda x: (path_lengths[x], x))
        social_wishes[person].extend(
            name
            for name in sorted_names
            if name not in social_wishes[person]
            and gender == genders[name]
            and name != person
        )

        # Fill in remaining same gender friends
        primary_names, secondary_names = _shuffle_names(
            genders, girls_names, boys_names, person
        )
        social_wishes[person].extend(
            name
            for name in primary_names
            if name not in social_wishes[person] and name != person
        )

        # Fill in close opposite gender friends
        social_wishes[person].extend(
            name
            for name in sorted_names
            if name not in social_wishes[person] and name != person
        )

        # Fill in remaining opposite gender friends
        social_wishes[person].extend(
            name
            for name in secondary_names
            if name not in social_wishes[person]
        )


def _remove_asocialites(
    df: DataFrame, wishes: Wishes, verbose: bool = False
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


def get_wishes(df: DataFrame) -> tuple[Wishes, Wishes, Wishes]:
    academic_wishes, social_wishes = _create_wishes(df)
    _remove_asocialites(df, social_wishes, verbose=True)
    initial_wishes = deepcopy(social_wishes)
    _fill_wishes(df, academic_wishes, social_wishes)
    return academic_wishes, initial_wishes, social_wishes


def remove_well_matched(
    social_wishes: MutableMapping[str, list[str]],
    initial_wishes: MutableMapping[str, list[str]],
    well_matched: Iterable[str],
) -> None:

    for person in well_matched:
        social_wishes.pop(person, None)
        initial_wishes.pop(person, None)

        for friend_list in social_wishes.values():
            friend_list.remove(person)

        for friend_list in initial_wishes.values():
            if person in friend_list:
                friend_list.remove(person)
