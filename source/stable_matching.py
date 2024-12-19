import json
from collections.abc import Container, Iterable, Mapping

from matching.games import StableRoommates

from source.constants import MATCHING_FILE
from source.helpers.bidict import Bidict


def stable_roommates(wishes: Mapping[str, Iterable[str]]) -> Bidict:
    game = StableRoommates.create_from_dictionary(wishes)
    matching = game.solve()
    return Bidict({str(k): str(v) for k, v in matching.items()})


def score_matching(
    initial_wishes: Mapping[str, Container[str]], matching: Bidict
) -> int:
    return sum(
        matching[person] in wish_list
        for person, wish_list in initial_wishes.items()
    )


def export_matching(matching: Bidict) -> None:
    with open(MATCHING_FILE, "w", encoding="utf-8") as file:
        json.dump(matching.d, file, ensure_ascii=False, indent=4)

    print(f"Wrote matching to {MATCHING_FILE!r}.")


def import_matching() -> Bidict:
    with open(MATCHING_FILE, encoding="utf-8") as file:
        return Bidict(json.load(file))
