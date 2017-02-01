from __future__ import print_function
import numpy as np
from scipy.optimize import linprog
import subprocess
import sys


for index in range(10000):

    n, m = np.random.randint(1, 8, size=(2,))
    A = np.random.randint(-100, 100, size=(n, m,))
    b = np.random.randint(-1000000, 1000000, size=(n,))
    c = np.random.randint(-100, 100, size=m)

    # Specific example that you want to test
    # n = 4
    # m = 6
    # A = np.array([[21, -67, 85, 82, 35, 20], [18, -66, -53, -37, 43, -37], [10, 76, -75, -88, -3, -53], [81, 36, 42, -33, -4, 86]])
    # b = np.array([337381, -810669, 901701, 971043])
    # c = np.array([-77, 13, -84, 58, 79, 72])

    print("======= Start New ========")
    print("Index: %s" % index)
    print(n, m)
    for i in range(n):
        print(*(A[i][j] for j in range(m)))
    print(*b)
    print(*c)
    print()

    proc = subprocess.Popen([sys.executable, 'diet3.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    print(n, m, file=proc.stdin)
    for i in range(n):
        print(*(A[i][j] for j in range(m)), file=proc.stdin)
    print(*b, file=proc.stdin)
    print(*c, file=proc.stdin)
    stdoutdata, _ = proc.communicate()
    assert proc.returncode == 0

    stdout_lines = stdoutdata.splitlines()
    print("======= My Solution ==================")
    print(stdoutdata, end='')

    print("======= Lin Solution ==================")
    solution_x = None
    linprog_res = linprog(-c, A_ub=A, b_ub=b, options={'tol': 1e-3})
    if linprog_res.status == 3:
        assert stdout_lines[0] == 'Infinity'
    elif linprog_res.status == 2:
        assert stdout_lines[0] == 'No solution'
    elif linprog_res.status == 0:
        solution_x = linprog_res.x
        print('x_ref =', ' '.join(list(map(lambda x: '%.18f' % float(x), solution_x))))
        assert stdout_lines[0] == 'Bounded solution'

    if stdout_lines[0] == 'Bounded solution':
        my_solution_x = np.array([float(num_str) for num_str in stdout_lines[1].split(' ')])
        assert len(my_solution_x) == len(solution_x)
        # Verify that all inequalities are satisfied.
        assert (np.dot(A, my_solution_x) <= b + 1e-3).all()

    if stdout_lines[0] == 'Bounded solution':
        max_my_program = np.dot(c, my_solution_x)
    else:
        max_my_program = stdout_lines[0]
    print('my solution =', max_my_program)

    if linprog_res.status == 0:
        max_ref = np.dot(c, solution_x)
    elif linprog_res.status == 3:
        max_ref = 'Infinity'
    elif linprog_res.status == 2:
        max_ref = 'No solution'
    print('lin solution =', max_ref)

    # Total pleasure differs from the optimum by at most 1e-3.
    if stdout_lines[0] == 'Bounded solution':
        assert (abs(max_my_program - max_ref) <= 1e-3)

    print()
