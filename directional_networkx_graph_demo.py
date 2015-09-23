import networkx as nx


def all_relatives(relation_fn, node, flatten):
    nodes = relation_fn(node)
    sub_nodes = [all_relatives(relation_fn, n, flatten) for n in nodes]
    if flatten:
        sub_nodes = [y for x in sub_nodes for y in x]
    return nodes + [n for n in sub_nodes if n]


def all_predecessors(graph, node, flatten=True):
    return all_relatives(graph.predecessors, node, flatten)


def all_successors(graph, node, flatten=True):
    return all_relatives(graph.successors, node, flatten)


def main():

    """
    Making a graph with this shape:

        A           B           C
        **          *          *
        *  *        *        *
        *    *      *      *
        *      *    *    *
        *        *  *  *
        *           *
        G           D
         *          *
          *         E
           *      *
            *    *
             * *
              F

    """

    G = nx.DiGraph()
    G.add_edge('A', 'D')
    G.add_edge('B', 'D')
    G.add_edge('C', 'D')
    G.add_edge('D', 'E')
    G.add_edge('E', 'F')
    G.add_edge('A', 'G')
    G.add_edge('G', 'F')

    print(G.successors('A'))

    print(G.predecessors('D'))
    print(G.predecessors('F'))
    print(G.predecessors('G'))

    print(all_predecessors(G, 'F'))
    print(all_successors(G, 'A'))
    print(all_predecessors(G, 'F', False))
    print(all_successors(G, 'A', False))


if __name__ == '__main__':
    main()
