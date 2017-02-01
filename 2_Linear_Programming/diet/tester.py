import random

import numpy as np
from scipy import optimize

import diet_p

NO_SOL = "No solution"
BOUNDED = "Bounded solution"
INF = "Infinity"

maps = {NO_SOL: -1, BOUNDED: 0, INF: 1}

def main():
    for _ in range(1000):
        n = random.randint(1, 8)
        m = random.randint(1, 8)
        A = []
        for __ in range(n):
            A.append([random.randint(-100, 100) for ___ in range(m)])
        b = [random.randint(-1000000, 1000000) for ___ in range(n)]
        c = [random.randint(-100, 100) for i in range(m)]
        result = solve(n, m, A, b, c)
        if result.status == 3:
            result_t = 1
        elif result.status == 0:
            result_t = 0
        else:
            result_t = -1
        for i in range(n):
            A[i].append(b[i])
        inf_bound = []
        for i in range(m -1):
            inf_bound.append(1.0)
        inf_bound.append(diet_p.BIG)
        A.append(inf_bound)
        ans_t, ans_x = diet_p.simplex([A, c])
        ans_t = maps[ans_t]
        ans_x = [x if x != -0.0 else 0.0 for x in ans_x]
        assert result_t == ans_t
        if result_t == 0:
            for x, y in zip(ans_x, result.x):
                assert abs(x - y) <= 1.0e-3


def solve(n, m, A, b, c):
    print("Solving: ", n, m, A, b, c)
    return optimize.linprog(
        -np.array(c),
        A_ub=np.array(A),
        b_ub=np.array(b),
        bounds=[(0, None)] * m,
        options={'tol': 1e-3},
    )

if __name__ == '__main__':
    main()
