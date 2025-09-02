import numpy as np

def evaluate_zdt1(variables):
    x1 = variables[0]
    n = len(variables)
    g = 1 + 9 * np.sum(variables[1:]) / (n - 1)
    f1 = x1
    f2 = g * (1 - np.sqrt(x1 / g))
    return [f1, f2]

class ZDT1:
    def __init__(self, n_variables=30):
        self.n_variables = n_variables
        self.bounds = [(0.0, 1.0)] * n_variables

    def evaluate(self, variables):
        return evaluate_zdt1(variables)
