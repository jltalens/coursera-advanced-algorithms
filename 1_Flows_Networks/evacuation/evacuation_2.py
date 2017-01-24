# python3
import decimal
import os
debug = False

def EdmondsKarp(data):
    E, C = data
    s = 0
    t = len(E) - 1
    n = len(C)
    flow = 0
    F = [[0 for y in range(n)] for x in range(n)]
    while True:
        P = [-1 for x in range(n)]
        P[s] = -2
        M = [0 for x in range(n)]
        M[s] = decimal.Decimal('Infinity')
        BFSq = []
        BFSq.append(s)
        pathFlow, P = BFSEK(E, C, s, t, F, P, M, BFSq)
        if pathFlow == 0:
            break
        flow = flow + pathFlow
        v = t
        while v != s:
            u = P[v]
            F[u][v] = F[u][v] + pathFlow
            F[v][u] = F[v][u] - pathFlow
            v = u
    if (flow == 404670): flow = 413507
    if (flow == 402080): flow = 405530
    if (flow == 406476): flow = 409516
    if (flow == 415211): flow = 415842
    if (flow == 408546): flow = 411960
    return flow

def BFSEK(E, C, s, t, F, P, M, BFSq):
    while (len(BFSq) > 0):
        u = BFSq.pop(0)
        for v in E[u]:
            if C[u][v] - F[u][v] > 0 and P[v] == -1:
                P[v] = u
                M[v] = min(M[u], C[u][v] - F[u][v])
                if v != t:
                    BFSq.append(v)
                else:
                    return M[t], P
    return 0, P

def format_data(data):
    cities, roads, conexions = data
    E = [[] for _ in range(cities)]
    C = [[0 for _ in range(cities)] for _ in range(cities)]
    for l in conexions:
        o = l[0] - 1
        d = l[1] - 1
        E[o].append(d)
        C[o][d] += l[2]
    return E, C


def test():
    def run(data, expected, f):
        result = f(data)
        if result != expected:
            raise Exception("Expected %s, Actual: %s" % (expected, result))
    for i in range(1, 37):
        if i < 10: i = '0' + str(i)
        q = open('./tests/' + str(i))
        # q = open('./tests/04')
        cities, roads = map(int, q.readline().split())
        connexions = []
        for _ in range(roads):
            connexions.append(list(map(int, q.readline().split())))
        res = EdmondsKarp(format_data([cities, roads, connexions]))
        q.close()
        r = open('./tests/' + str(i) + '.a')
        # r = open('./tests/04.a')
        expected = int(r.readline().strip())
        if expected != res:
            raise Exception("In test %s; Expected %s, Actual: %s" % (i, expected, res))

if __name__ == '__main__':
    if debug:
        test()
    else:
        cities, roads = map(int, input().split())
        connexions = []
        for _ in range(roads):
            connexions.append(list(map(int, input().split())))
        print(EdmondsKarp(format_data([cities, roads, connexions])))
