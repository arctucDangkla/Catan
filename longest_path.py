from Nodes_and_structures_map import *


def temp_name(edge: Edge, player, last: list, visited: list):
    visited.append(edge)
    options = []
    new = []
    for node in edge.nodes:
        if node not in last:
            new.append(node)
            for path in node.roads:
                if path not in visited and path.player == player:
                    options.append(path)



    if len(options) == 0:
        return 1
    elif len(options) == 1:
        return 1 + temp_name(options[0], player, new, visited)
    else:
        a = temp_name(options[0], player, new, visited)
        b = temp_name(options[1], player, new, visited)

        if b > a:
            return b + 1
        return a + 1

