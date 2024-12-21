import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph, Graph

from source.constants import Wishes


def add_wish_edge(wishes: Wishes, wish_index: int, graph: Graph) -> None:
    if wish_index < 0:
        raise ValueError("Invalid wish index.")

    for name, friends in wishes.items():
        if len(friends) <= wish_index:
            continue

        graph.add_edge(name, friends[wish_index])


def plot_graphs(graph: Graph) -> None:
    components = (
        nx.weakly_connected_components(graph)
        if isinstance(graph, DiGraph)
        else nx.connected_components(graph)
    )

    for i, component in enumerate(components, 1):
        subgraph = graph.subgraph(component)

        plt.figure(figsize=(12, 6))
        nx.draw(subgraph, with_labels=True)
        plt.title(f"Roommate Wishes - Component {i}")
        plt.show()
