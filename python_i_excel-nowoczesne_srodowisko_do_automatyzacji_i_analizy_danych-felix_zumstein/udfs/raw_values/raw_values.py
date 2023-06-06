import numpy as np
import xlwings as xw


@xw.func
@xw.ret("raw")
def randn(i=1000, j=1000):
    """Zwraca tablicę o wymiarach (i, j) z liczbami pseudolosowymi
    o rozkładzie normalnym dostarczoną przez funkcję NumPy random.randn
    """
    return np.random.randn(i, j)
