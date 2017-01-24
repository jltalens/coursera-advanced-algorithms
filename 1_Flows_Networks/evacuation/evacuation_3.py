# python3
from collections import deque, defaultdict
debug = True
inf = float('inf')

def bfs_aug(G, H, s, t, f):
    P, Q, F = {s: None}, deque([s]), {s: inf}
    def label(inc):
        if v in P or inc <= 0:
            return
        F[v], P[v] = min(F[u], inc), u
        Q.append(v)
    while Q:
        u = Q.popleft()
        if u == t:
            return P, F[t]
        for v in G[u]:
            label(G[u][v]-f[u, v])
        for v in H[u]:
            label(f[v, u])
    return None, 0

def tr(G):
    GT = {}
    for u in range(len(G)):
        GT[u] = set()
    for u in range(len(G)):
        for v in G[u]:
            GT[v].add(u)
    return GT

def ford_fulkerson(data):
    G, s, t = data
    H, f = tr(G), defaultdict(int)
    max_flow = 0
    while True:
        P, c = bfs_aug(G, H, s, t, f)
        max_flow += c
        if c == 0:
            return max_flow
        u = t
        while u != s:
            u, v = P[u], u
            if v in G[u]:
                f[u, v] += c
            else:
                f[v, u] -= c

def test():
    def run(data, expected, f=ford_fulkerson):
        assert f(data) == expected
    edges = [{1: 10000, 2: 10000}, {2: 1, 3: 10000}, {3: 10000}, {}]
    run([edges, 0, len(edges) -1], 20000)
    edges = [{1: 2, 2: 6}, {4: 5, 3: 1}, {1: 3, 3: 2}, {4: 1}, {}]
    run([edges, 0, len(edges) -1], 6)


if __name__ == '__main__':
    if debug:
        test()
    else:
        print(from_input())
