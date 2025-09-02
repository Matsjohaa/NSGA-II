import numpy as np
from problem import ZDT1
from individual import Individual
from utils import fast_non_dominated_sort, calculate_crowding_distance

class NSGA2:
    def __init__(self, n_variables=30, pop_size=100, generations=250):
        self.problem = ZDT1(n_variables)
        self.pop_size = pop_size
        self.generations = generations
        self.n_variables = n_variables

    def initialize_population(self):
        return [Individual(self.n_variables) for _ in range(self.pop_size)]

    def evaluate_population(self, population):
        for ind in population:
            ind.evaluate(self.problem)

    def tournament_selection(self, population):
        a, b = np.random.choice(population, 2, replace=False)
        if a.rank < b.rank or (a.rank == b.rank and a.crowding_distance > b.crowding_distance):
            return a
        else:
            return b

    def crossover(self, parent1, parent2, eta=20):
        child1 = Individual(self.n_variables)
        child2 = Individual(self.n_variables)
        for i in range(self.n_variables):
            u = np.random.rand()
            if u <= 0.5:
                beta = (2*u)**(1/(eta+1))
            else:
                beta = (1/(2*(1-u)))**(1/(eta+1))
            child1.variables[i] = 0.5*((1+beta)*parent1.variables[i] + (1-beta)*parent2.variables[i])
            child2.variables[i] = 0.5*((1-beta)*parent1.variables[i] + (1+beta)*parent2.variables[i])
            child1.variables[i] = np.clip(child1.variables[i], 0, 1)
            child2.variables[i] = np.clip(child2.variables[i], 0, 1)
        return child1, child2

    def mutate(self, individual, eta=20, mutation_rate=1.0/30):
        for i in range(self.n_variables):
            if np.random.rand() < mutation_rate:
                u = np.random.rand()
                if u < 0.5:
                    delta = (2*u)**(1/(eta+1)) - 1
                else:
                    delta = 1 - (2*(1-u))**(1/(eta+1))
                individual.variables[i] += delta
                individual.variables[i] = np.clip(individual.variables[i], 0, 1)

    def run(self):
        population = self.initialize_population()
        self.evaluate_population(population)
        for gen in range(self.generations):
            fronts = fast_non_dominated_sort(population)
            for front in fronts:
                calculate_crowding_distance(front)
            offspring = []
            while len(offspring) < self.pop_size:
                p1 = self.tournament_selection(population)
                p2 = self.tournament_selection(population)
                c1, c2 = self.crossover(p1, p2)
                self.mutate(c1)
                self.mutate(c2)
                offspring.extend([c1, c2])
            offspring = offspring[:self.pop_size]
            self.evaluate_population(offspring)
            combined = population + offspring
            fronts = fast_non_dominated_sort(combined)
            new_population = []
            for front in fronts:
                calculate_crowding_distance(front)
                if len(new_population) + len(front) > self.pop_size:
                    front.sort(key=lambda x: (-x.crowding_distance, x.rank))
                    new_population.extend(front[:self.pop_size - len(new_population)])
                    break
                else:
                    new_population.extend(front)
            population = new_population
            if (gen+1) % 10 == 0:
                print(f"Generation {gen+1} completed.")
        return population
