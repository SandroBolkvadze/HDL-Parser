from collections import defaultdict, deque

from core.chips.chip import Chip
from core.chips.chip_part import ChipPart


def topo_sort(nodes: list[int], graph: dict[int, list[int]]) -> list[int]:
    ins: dict[int, int] = defaultdict(int)
    topo_sorted: list[int] = []

    for u in nodes:
        for v in graph[u]:
            ins[v] += 1

    q = deque([u for u in nodes if ins[u] == 0])

    while len(q) > 0:
        u = q.popleft()
        topo_sorted.append(u)
        for v in graph[u]:
            ins[v] -= 1
            if ins[v] == 0:
                q.append(v)

    return topo_sorted


def build_graph_for(
    chip_parts: list[ChipPart], chips: dict[str, Chip]
) -> dict[int, list[int]]:
    graph: defaultdict[int, list[int]] = defaultdict(list)

    for i, chip_part_i in enumerate(chip_parts):
        outs = {
            connection.right
            for connection in chip_part_i.chip_connections
            if connection.left in chips[chip_part_i.chip_name].get_output_pins()
        }
        for j, chip_part_j in enumerate(chip_parts):
            if j == i:
                continue
            ins = {
                connection.right
                for connection in chip_part_j.chip_connections
                if connection.left in chips[chip_part_j.chip_name].get_input_pins()
            }
            if len(outs & ins):
                graph[i].append(j)

    return graph
