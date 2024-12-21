import json
from typing import TypeAlias

from matching.games import StableRoommates

from source.constants import MATCHING_FILE, Wishes


Matching: TypeAlias = dict[str, str]


def stable_roommates(wishes: Wishes) -> Matching:
    game = StableRoommates.create_from_dictionary(wishes)
    matching = game.solve()
    return {str(k): str(v) for k, v in matching.items()}


def score_matching(initial_wishes: Wishes, matching: Matching) -> int:
    return sum(
        matching[person] in wish_list
        for person, wish_list in initial_wishes.items()
    )


def export_matching(matching: Matching) -> None:
    matching = {k: v for k, v in matching.items() if k < v}

    with open(MATCHING_FILE, "w", encoding="utf-8") as file:
        json.dump(matching, file, ensure_ascii=False, indent=4)

    print(f"Wrote matching to {MATCHING_FILE!r}.")


def import_matching() -> Matching:
    with open(MATCHING_FILE, encoding="utf-8") as file:
        matching: Matching = json.load(file)
        return matching | {v: k for k, v in matching.items()}
