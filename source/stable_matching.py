import json
from typing import TypeAlias

from matching.games import StableRoommates

from source.constants import MATCHING_FILE, Wishes


Matching: TypeAlias = dict[str, str]


def stable_roommates(wishes: Wishes) -> Matching:
    game = StableRoommates.create_from_dictionary(wishes)
    matching = game.solve()

    if None in matching.values():
        raise ValueError("Not all participants could be matched.")

    return {k.name: v.name for k, v in matching.items()}


def score_matching(initial_wishes: Wishes, matching: Matching) -> int:
    count = 0

    for person, wish_list in initial_wishes.items():
        if matching[person] in wish_list:
            count += 1
        else:
            print(
                f"{person} matched with {matching[person]}, but wanted: "
                f"{', '.join(wish_list)}."
            )

    return count


def export_matching(matching: Matching) -> None:
    matching = {k: v for k, v in matching.items() if k < v}

    with open(MATCHING_FILE, "w", encoding="utf-8") as file:
        json.dump(matching, file, ensure_ascii=False, indent=4, sort_keys=True)

    print(f"Wrote matching to {MATCHING_FILE!r}.")


def import_matching() -> Matching:
    with open(MATCHING_FILE, encoding="utf-8") as file:
        matching: Matching = json.load(file)

    return matching | {v: k for k, v in matching.items()}
