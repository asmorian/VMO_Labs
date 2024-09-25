import numpy as np
import random
import copy


def create_symmetric_path_matrix(matrix_size, lower_limit, upper_limit):
    # Создаём случайную матрицу
    matrix = np.random.randint(lower_limit, upper_limit, size=(matrix_size, matrix_size))

    # Делаем матрицу симметричной
    symmetric_matrix = np.triu(matrix) + np.triu(matrix, 1).T

    # Устанавливаем диагональные элементы в 0 (нет путей от узла к самому себе)
    np.fill_diagonal(symmetric_matrix, 0)

    return symmetric_matrix


def create_logs(message):
    with open('lab_7_ways.txt', 'a') as log_file:
        log_file.write(message + "\n")


class Individual:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = len(matrix)
        self.genes = []
        self.fitness = 0

    def create_random_individual(self, start_poss):
        self.genes = list(range(1, self.size + 1))
        self.genes.remove(start_poss)
        random.shuffle(self.genes)
        self.genes.insert(0, start_poss)
        self.genes.append(start_poss)

    def crossover(self, parent2):
        point = random.randint(2, self.size - 2)
        child = copy.deepcopy(self)

        first_half = self.genes[:point]
        second_half = []
        for item in parent2.genes:
            if item not in first_half:
                second_half.append(item)
        second_half.append(first_half[0])

        child.genes = first_half + second_half
        return child, point

    def mutation(self):
        first = random.randint(1, self.size - 2)
        second = random.randint(1, self.size - 2)
        while first == second:
            second = random.randint(1, self.size - 2)

        child = copy.deepcopy(self)
        child.genes[first], child.genes[second] = child.genes[second], child.genes[first]
        # print(f"Было  - {self.genes}")
        # print(f"Стало - {child.genes} - Обмен на {first + 1} <-> {second + 1}")
        return child

    def evaluate_fitness(self):
        ways_list = []
        intermediate_fitness_list = []

        for _ in range(self.size):
            ways_list.append([self.genes[_], self.genes[_ + 1]])

        for way in ways_list:
            intermediate_fitness_list.append(self.matrix[way[0] - 1][way[1] - 1])

        self.fitness = sum(intermediate_fitness_list)
        return self.fitness


class GeneticAlg:
    def __init__(self, matrix, population_size, max_repeats, crossover_prob, mutation_prob, start_poss):
        self.matrix = matrix
        self.population_size = population_size
        self.max_repeats = max_repeats
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.start_poss = start_poss
        self.population = [Individual(self.matrix) for _ in range(population_size)]

        for item in self.population:
            item.create_random_individual(start_poss)

        self.best_individual = None
        self.best_fitness = float('inf')
        self.repeats = 1
        self.iteration = 1
        self.logs_cross = ''
        self.logs_mutated = ''

    def evaluate_population(self):
        population_fitness = []
        for item in self.population:
            population_fitness.append(item.evaluate_fitness())

        new_best_fitness = min(population_fitness)
        new_best_individual = self.population[population_fitness.index(new_best_fitness)]

        if new_best_fitness < self.best_fitness:
            self.best_individual = new_best_individual
            self.best_fitness = new_best_fitness
            self.repeats = 1
        elif new_best_fitness == self.best_fitness:
            self.best_individual = new_best_individual
            self.repeats += 1

        return population_fitness

    def create_new_population(self):
        new_population = []

        def generate_random_parents_2(parent1_id):
            while True:
                parent21_id = random.randint(0, self.population_size - 1)
                parent22_id = random.randint(0, self.population_size - 1)
                if parent21_id != parent1_id and parent21_id != parent22_id and parent22_id != parent1_id:

                    if self.population[parent21_id].fitness < self.population[parent22_id].fitness:
                        return parent21_id
                    elif self.population[parent21_id].fitness > self.population[parent22_id].fitness:
                        return parent22_id
                    else:
                        return min([parent21_id, parent22_id])

        for item in self.population:
            ind1 = self.population.index(item)
            new_individual = copy.deepcopy(item)

            trigger = random.random()
            if trigger < self.crossover_prob:
                second_parent_id = generate_random_parents_2(ind1)
                new_individual, point = item.crossover(self.population[second_parent_id])

            trigger = random.random()
            if trigger < self.mutation_prob:
                new_individual = item.mutation()

            if item.evaluate_fitness() < new_individual.evaluate_fitness():
                new_population.append(item)
            else:
                new_population.append(new_individual)

        self.population = new_population

    def run(self):
        create_logs(f"Ways =\n {self.matrix}\n")
        while self.repeats < self.max_repeats:
            fitness = self.evaluate_population()
            create_logs(f"Iteration {self.iteration} - Best Fitness: {self.best_fitness}")
            create_logs(f"Best Individual: {self.best_individual.genes}\n")
            for i in range(len(fitness)):
                create_logs(
                    f"Individual {self.iteration}/{i + 1} = {self.population[i].genes} ---> Fitness {fitness[i]}")

            self.iteration += 1
            create_logs('\n')

            self.create_new_population()
