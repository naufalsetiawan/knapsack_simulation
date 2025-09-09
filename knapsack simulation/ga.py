import random

def knapsack_ga(weights, values, capacity, pop_size=50, generations=100, crossover_rate=0.8, mutation_rate=0.1):
    num_items = len(weights)

    # def generate_individual():
    #     return [random.randint(0, 1) for _ in range(num_items)] 
    
    def generate_individual():
        individual = [0] * num_items
        total_weight = 0
        indices = list(range(num_items))
        random.shuffle(indices)
        for i in indices:
            if total_weight + weights[i] <= capacity:
                if random.random() < 0.5:
                    individual[i] = 1
                    total_weight += weights[i]
        return individual


    def fitness(individual):
        total_weight = sum(individual[i] * weights[i] for i in range(num_items))
        total_value = sum(individual[i] * values[i] for i in range(num_items))
        if total_weight > capacity:
            return 0
        return total_value

    def selection(population):
        max_fit = sum(fitness(ind) for ind in population)
        if max_fit == 0:
            return random.choice(population)
        pick = random.uniform(0, max_fit)
        current = 0
        for ind in population:
            current += fitness(ind)
            if current > pick:
                return ind

    def crossover(parent1, parent2):
        if random.random() < crossover_rate:
            point = random.randint(1, num_items - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1[:], parent2[:]

    def mutate(individual):
        for i in range(num_items):
            if random.random() < mutation_rate:
                individual[i] = 1 - individual[i]
        return individual

    # --- Main GA ---
    population = [generate_individual() for _ in range(pop_size)]
    best_fitness_history = []
    stagnation_limit = 20

    for gen in range(generations):
        population = sorted(population, key=fitness, reverse=True)
        best_ind = population[0]
        best_fit = fitness(best_ind)
        best_fitness_history.append(best_fit)

        if len(best_fitness_history) > stagnation_limit:
            recent = best_fitness_history[-stagnation_limit:]
            if max(recent) == min(recent):
                break

        next_generation = [best_ind]
        while len(next_generation) < pop_size:
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            if len(next_generation) < pop_size:
                next_generation.append(mutate(child2))
        population = next_generation

    best_solution = max(population, key=fitness)
    return best_solution, fitness(best_solution), best_fitness_history
