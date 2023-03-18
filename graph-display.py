import matplotlib.pyplot as plt
import networkx as nx
import csv
from os import listdir

def load_knowledge_graph(filepath):

    G = nx.MultiDiGraph()

    with open("graph/" + filepath) as datafile:
        for line in csv.reader(datafile):
            subj, verb, obj = line
            verb = {"взаимосвязан с": 20.0,
                    "имеет отношение к": 9.0,
                    "незначимо связан с": 3.0}[verb]
            G.add_edge(
                subj.replace("<", "").title(),
                obj.replace("<", "").title(),
                verb=verb
            )

    return G

def draw_graph(filepath):
    G = load_knowledge_graph(filepath)

    # make new undirected graph H without multi-edges
    H = nx.Graph(G)

    edgewidth = [d["verb"] for u, v, d in H.edges(data=True)]
    nodesize = [0 for v in H]

    # Generate layout for visualization
    pos = nx.kamada_kawai_layout(H)

    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot()
    plt.box(False)

    # Visualize graph components
    nx.draw_networkx_edges(H, pos, alpha=0.3, width=edgewidth, edge_color="m")
    nx.draw_networkx_nodes(H, pos, node_size=nodesize, node_color="#210070", alpha=0.9)
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    nx.draw_networkx_labels(H, pos, font_size=10, bbox=label_options)

    # Title/legend
    font = {"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 14}
    ax.set_title(filepath, font)
    # Change font color for legend
    font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    # fig.axis("off")
    fig.savefig("graph-images/" + filepath + ".png")

if __name__ == "__main__":
    for filepath in listdir("graph/"):
        print(filepath)
        if filepath + ".png" in listdir("graph-images/"):
            continue
        draw_graph(filepath)
