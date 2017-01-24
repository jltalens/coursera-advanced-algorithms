# python3
import itertools
debug = True
# n, m = map(int, input().split())
# edges = [ list(map(int, input().split())) for i in range(m) ]
n, m = 4, 6
edges = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
colors = 3

"""
All colored
(x11 v x21 v x31)
(x12 v x22 v x32)
(x13 v x23 v x33)

x1 - x2
(!x11 v !x21)
(!x12 v !x22)
(!x13 v !x23)

R , 1 -> 1
A , 1 -> 2
V , 1 -> 3

R, 2 -> 3
A, 2 -> 5
V, 2 -> 7

R, 3 -> 6
A, 3 -> 7
V, 3 -> 8
"""
def no(x1):
    return x1 * -1

def two_vertex_different_colors(x1, x2):
    res = []
    for i in range(1, colors + 1):
        res.append([no(x1 * i), no(x2 * i + 1)])
    print(res)
    return res

def test():
    assert no(3) == -3
    assert two_vertex_different_colors(1, 2) == [[-1, -4], [-2, -5], [-3, -6]]

if __name__ == "__main__":
    if debug:
        test()
    else:
        pass
#
# total_variables = n * colors
# vertex_one_color = ""
# for i in range(n):
#     for j in range(colors):
#         vertex_one_color =+ ""
#
# variable_cond = " ".join([str(i) for i in range(1, n +1)]) + " 0"
# color_cond = ""
# i = 1
# for e in edges:
#     reverse_sign = list(map(lambda x: str(x * -1), e))
#     color_cond += " ".join(reverse_sign) + " 0\n"
#     i += 1
# print("p cnf %s %s" % (str(n), str(i)))
# print(variable_cond)
# print(color_cond[:-1])
# This solution prints a simple satisfiable formula
# and passes about half of the tests.
# Change this function to solve the problem.
# def printEquisatisfiableSatFormula():
#     print("3 2")
#     print("1 2 0")
#     print("-1 -2 0")
#     print("1 -2 0")

# printEquisatisfiableSatFormula()
