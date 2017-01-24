# python3
from itertools import chain
debug = False

def tr(G):
    GT = {}
    for u in range(len(G)):
        GT[u] = set()                   # Get all the nodes in there
    for u in range(len(G)):
        for v in G[u]:
            GT[v].add(u)                        # Add all reverse edges
    return GT


def match(G, X, Y):                             # Maximum bipartite matching
    H = tr(G)                                   # The transposed graph
    S, T, M = set(X), set(Y), set()             # Unmatched left/right + match
    while S:                                    # Still unmatched on the left?
        s = S.pop()                             # Get one
        Q, P = {s}, {}                          # Start a traversal from it
        while Q:                                # Discovered, unvisited
            u = Q.pop()                         # Visit one
            if u in T:                          # Finished augmenting path?
                T.remove(u)                     # u is now matched
                break                           # and our traversal is done
            forw = (v for v in G[u] if (u, v) not in M)  # Possible new edges
            back = (v for v in H[u] if (v, u) in M)      # Cancellations
            for v in chain(forw, back):         # Along out- and in-edges
                if v in P: continue             # Already visited? Ignore
                P[v] = u                        # Traversal predecessor
                Q.add(v)                        # New node discovered
        while u != s:                           # Augment: Backtrack to s
            u, v = P[u], u                      # Shift one step
            if v in G[u]:                       # Forward edge?
                M.add((u, v))                    # New edge
            else:                               # Backward edge?
                M.remove((v, u))                 # Cancellation
    return M                                    # Matching -- a set of edges

def bipartite_match(data):
    G, flights, crew = data
    lF = len(flights)
    M = match(G, flights, crew)
    assign = [-1 for _ in range(lF)]
    for p in M:
        assign[p[0]] = p[1] - lF + 1
    return assign

def from_input():
    len_flights, len_crew = map(int, input().split())
    flights = [i for i in range(len_flights)]
    crew = [i + len_flights for i in range(len_crew)]
    edges = [[] for _ in range(len_flights + len_crew)]
    for i in range(len_flights):
        crew_assign = list(map(int, input().split()))
        for j in range(len(crew_assign)):
            if crew_assign[j] == 1:
                edges[i].append(j + len_flights)
    return bipartite_match([edges, flights, crew])

def test():
    def run(data, expected, f=bipartite_match):
        assert sorted(f(data)) == sorted(expected)
    for f in range(1, 31):
        if f < 10:
            f = '0' + str(f)
        q = open('tests/' + f)
        len_flights, len_crew = map(int, q.readline().split())
        flights = [i for i in range(len_flights)]
        crew = [i + len_flights for i in range(len_crew)]
        edges = [[] for _ in range(len_flights + len_crew)]
        for i in range(len_flights):
            crew_assign = list(map(int, q.readline().split()))
            for j in range(len(crew_assign)):
                if crew_assign[j] == 1:
                    edges[i].append(j + len_flights)
        q.close()
        q = open('tests/' + f + '.a')
        expected = list(map(int, q.readline().split()))
        q.close()
        run([edges, flights, crew], expected)

    edges = [[3, 4, 6], [4], [], [], [], [], []]
    flights = [0, 1, 2]
    crew = [3, 4, 5, 6]
    run([edges, flights, crew], [1, 2, -1])
    # edges = [{1: 1, 2: 1, 3: 1}, {4: 1, 5: 1, 7: 1}, {5: 1}, {}, {8: 1}, {8: 1}, {8: 1}, {8: 1}, {}]
    # run([edges, 3, 4], [1, 2, -1])


if __name__ == '__main__':
    if debug:
        test()
    else:
        print(" ".join(list(map(str, from_input()))))
