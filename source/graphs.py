import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph, Graph
from pandas import DataFrame

from source.constants import (
    GENDER_COLUMN,
    GENDERS,
    NAME_COLUMN,
    WISH_COLUMNS,
    GraphPair,
    Wishes,
)


def add_wish_edge(
    df: DataFrame,
    wishes: Wishes,
    wish_index: int,
    graphs: GraphPair | None = None,
) -> GraphPair:
    if wish_index < 0 or wish_index >= len(WISH_COLUMNS):
        raise ValueError("Invalid wish index.")

    genders: dict[str, str] = dict(zip(df[NAME_COLUMN], df[GENDER_COLUMN]))
    graphs = graphs if graphs is not None else (Graph(), Graph())

    for name, friends in wishes.items():
        if len(friends) <= wish_index:
            continue

        graph = graphs[GENDERS.index(genders[name])]
        graph.add_edge(name, friends[wish_index])

    return graphs


def plot_graphs(graphs: GraphPair) -> None:
    for graph, gender in zip(graphs, GENDERS):
        components = (
            nx.weakly_connected_components(graph)
            if isinstance(graph, DiGraph)
            else nx.connected_components(graph)
        )

        for i, component in enumerate(components, 1):
            subgraph = graph.subgraph(component)

            plt.figure(figsize=(12, 6))
            nx.draw(subgraph, with_labels=True)
            plt.title(f"{gender} Roommate Wishes - Component {i}")
            plt.show()
