import networkx as nx
from matplotlib import pyplot as plt
from networkx import Graph
from pandas import DataFrame

from source.constants import GENDER_COLUMN, GENDERS, NAME_COLUMN, WISH_COLUMNS


def add_wish_edge(
    df: DataFrame,
    wishes: dict[str, list[str]],
    wish_index: int,
    graphs: tuple[Graph, Graph] | None = None,
) -> tuple[Graph, Graph]:
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


def plot_graphs(graphs: tuple[Graph, Graph]) -> None:
    for graph, gender in zip(graphs, GENDERS):
        for i, component in enumerate(nx.connected_components(graph), 1):
            subgraph = graph.subgraph(component)

            plt.figure(figsize=(12, 6))
            nx.draw(subgraph, with_labels=True)
            plt.title(f"{gender} Roommate Wishes - Component {i}")
            plt.show()
