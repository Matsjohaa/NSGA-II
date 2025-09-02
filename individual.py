import numpy as np

class Individual:
    def __init__(self, n_variables):
        self.n_variables = n_variables
        self.variables = np.random.rand(n_variables)
        self.objectives = [None, None]
        self.rank = None
        self.crowding_distance = 0.0
        self.dominated_solutions = []
        self.domination_count = 0
        self.front = None

    def evaluate(self, problem):
        self.objectives = problem.evaluate(self.variables)
