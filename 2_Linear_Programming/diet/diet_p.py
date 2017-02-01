from itertools import chain, combinations

debug = True
NO_SOL = "No solution"
BOUNDED = "Bounded solution"
INF = "Infinity"
BIG = 10000000000
SMALL = float('-Infinity')

def gauss(A):
    n = len(A)
    for i in range(n):
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k
        if A[maxRow][i] == 0:
            return False, []
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return True, x

def from_input():
    A = []
    n, m = map(int, input().split())
    for i in range(n):
        A += [list(map(float, input().split()))]
    b = list(map(float, input().split()))
    for i in range(len(A)):
        A[i].append(b[i])
    inf_bound = []
    for i in range(len(A[0])-1):
        inf_bound.append(1.0)
    inf_bound.append(BIG)
    A.append(inf_bound)
    c = list(map(float, input().split()))
    return A, c


def subsets(s, f):
    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    return filter(lambda x: len(x) == f, map(set, powerset(s)))

def to_str(x):
    return list(map(lambda a : '%.18f' % a, x))

def simplex(data):
    A, c = data
    t = NO_SOL
    sol = []
    lA = len(A)
    obj = SMALL
    if (len(A[0])-1 > lA):
        return INF, []
    for liq in subsets(range(lA), len(A[0])-1):
        #  solve the system of linear equations where each equation is one of the selected inequalities changed to equality
        subA = [A[i] for i in liq]
        has_sol, sol_subA = gauss(subA)
        # check whether this solution satis es all the other inequalities
        if has_sol and check_sol(sol_subA, A, liq):
            maxLocal = 0
            for i in range(len(sol_subA)):
                maxLocal += sol_subA[i] * c[i]
            if maxLocal > obj:
                obj = maxLocal
                sol = sol_subA
            is_bounded = True
            if lA - 1 in subA:
                is_bounded = False
    if obj != SMALL:
        t = INF
        if is_bounded:
            t = BOUNDED
    return t, to_str(sol)

def check_sol(sol, A, sub_set_idx):
    rowL = len(A[0])
    idx = [i for i in range(len(A)) if i not in sub_set_idx]
    for i in idx:
        sub_sol = 0
        for j in range(rowL -1):
            sub_sol += A[i][j] * sol[j]
        if (sub_sol > A[i][rowL-1] * 0.0003):
            return False
    return True


def test():
    def run(data, expected, f=simplex):
        result = f(data)
        if result[0] != expected[0] or result[1] != expected[1]:
            raise Exception("Expected %s, Actual: %s" % (expected, result))
    A = [[-1.0, -1.0, -1.0], [1.0, 0.0, 2.0], [0.0, 1.0, 2.0],  [1.0, 1.0, BIG]]
    c = [-1.0, 2.0]
    s = [BOUNDED, ["-0.000000000000000000", "2.000000000000000000"]]
    run([A, c], s)
    A = [[1.0, 1.0, 1.0], [-1.0, -1.0, -2.0],  [1.0, 1.0, BIG]]
    c = [1.0, 1.0]
    s = [NO_SOL, []]
    run([A, c], s)
    A = [[0.0, 0.0, 1.0, 3.0],  [1.0, 1.0, 1.0, BIG]]
    c = [1.0, 1.0, 1.0]
    s = [INF, []]
    run([A, c], s)
    print("Test passed")

if __name__ == '__main__':
    if debug:
        test()
    else:
        s = simplex(from_input())
        print(s[0])
        tmp = ""
        for i in s[1]:
            tmp += i + " "
        print(tmp[:-1])
