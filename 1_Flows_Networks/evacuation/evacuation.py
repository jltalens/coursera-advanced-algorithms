# python3
debug = True

def from_input():
    n, m = list(map(int, input().split()))
    edges = [[] for _ in range(n)]
    c = {}
    for _ in range(m):
        o, d, f = list(map(int, input().split()))
        o -= 1
        d -= 1
        edges[o].append(d)
        c[str(o) + '-' + str(d)] = f
    return edges, c


def ford_fulkenson(data):
    def search(s, t):
        queue[0] = s
        head = 0
        tail = 1
        previous[s] = -1
        visited[s] = 1
        print(flow, c, visited, edges)
        while head != tail:
            u = queue[head]
            head = (head + 1) % queue_size
            print(visited)
            visited[u] = 2
            for v in edges[u]:
                k = str(u) + '-' + str(v)
                if visited[v] == 0 and c[k] > flow[u][v]:
                    queue[tail] = v
                    tail = (tail + 1) % queue_size
                    visited[v] = 1
                    previous[v] = u
        print(visited, previous)
        return visited[s] != 0

    def processPath(s, t):
        increment = 10001
        v = s
        print(previous)
        while previous[v] != -1:
            k = str(previous[v]) + '-' + str(v)
            unit = c[k] - flow[previous[v]][v]
            if unit < increment:
                increment = unit
            v = previous[v]
        v = s
        while previous[v] != -1:
            flow[previous[v]][v] += increment
            flow[v][previous[v]] -= increment
            v = previous[v]
        return increment

    edges, c = data
    s = 0
    queue_size = len(edges)
    t = queue_size - 1
    queue = [0 for _ in range(queue_size)]
    visited = [0 for _ in range(queue_size)]
    previous = [0 for _ in range(queue_size)]
    # flow = [[] for _ in range(queue_size)]
    # for i in range(queue_size):
    #     flow[i] = flow[i] + [0 for _ in range(len(edges[i]))]
    flow = [[0 for _ in range(queue_size)] for _ in range(queue_size)]
    max_flow = 0
    while search(s, t):
        print("hello")
        max_flow += processPath(s, t)
        exit(1)
    return max_flow



def test():
    def run(data, expected, f=ford_fulkenson):
        assert f(data) == expected
    edges = [[1, 2], [2, 3], [3], []]
    c = {'1-2': 1, '2-3': 10000, '0-1': 10000, '0-2': 10000, '1-3': 10000}
    run([edges, c], 20000)


if __name__ == '__main__':
    if debug:
        test()
    else:
        print(from_input())
