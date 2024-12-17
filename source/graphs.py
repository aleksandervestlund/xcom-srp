from collections.abc import Iterable

import networkx as nx
from matplotlib import pyplot as plt
from networkx import Graph
from pandas import DataFrame

from source.constants import GENDER_COLUMN, GENDERS, NAME_COLUMN, WISH_COLUMNS


def create_graphs(
    df: DataFrame, wish_columns: Iterable[str] | None = None
) -> tuple[Graph, Graph]:
    graph_female: Graph = Graph()
    graph_male: Graph = Graph()
    graphs = (graph_female, graph_male)

    if wish_columns is None:
        wish_columns = WISH_COLUMNS

    for _, row in df.iterrows():
        name = row[NAME_COLUMN]
        gender = row[GENDER_COLUMN]
        graph = graphs[GENDERS.index(gender)]

        for wish in wish_columns:
            friend = row[wish]

            if isinstance(friend, str):
                graph.add_edge(name, friend)

    return graphs


def plot_graphs(graphs: Iterable[Graph]) -> None:
    for graph, gender in zip(graphs, GENDERS, strict=True):
        for i, component in enumerate(nx.connected_components(graph), 1):
            subgraph = graph.subgraph(component)

            plt.figure(figsize=(12, 6))
            nx.draw(subgraph, with_labels=True)
            plt.title(f"{gender} Roommate Wishes - Component {i}")
            plt.show()
