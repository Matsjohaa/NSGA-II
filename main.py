from nsga2 import NSGA2
import matplotlib.pyplot as plt

if __name__ == "__main__":
    nsga2 = NSGA2(n_variables=30, pop_size=100, generations=100)
    final_population = nsga2.run()
    # Extract objectives
    f1 = [ind.objectives[0] for ind in final_population]
    f2 = [ind.objectives[1] for ind in final_population]
    # Plot Pareto front
    plt.scatter(f1, f2, s=10)
    plt.xlabel('Objective 1 (f1)')
    plt.ylabel('Objective 2 (f2)')
    plt.title('NSGA-II ZDT1 Pareto Front')
    plt.show()
