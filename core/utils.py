from collections import deque, defaultdict

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
