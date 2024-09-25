import random
import copy


class Individual:
    def __init__(self, tasks, proc_num):
        self.tasks = tasks
        self.proc_num = proc_num
        self.length = len(tasks)
        self.genes = []
        self.fitness = None

    # Функция создания нулевой особи
    def initial(self):
        self.genes = [random.randint(0, 255) for _ in range(self.length)]

    # Функция просчёта эффективности особи
    def evaluate_fitness(self):
        interval_size = 255 // self.proc_num
        processors = [[] for _ in range(self.proc_num)]

        # Функция для определения процессора по числу
        def get_processor_index(number):
            return min(number // interval_size, self.proc_num - 1)

        # Распределяем числа по процессорам
        for i in range(self.length):
            processor_index = get_processor_index(self.genes[i])
            processors[processor_index].append(self.tasks[i])

        load = []
        for proc in processors:
            load.append(sum(proc))

        self.fitness = max(load)
        return self.fitness

    def mutate(self):
        start_fit = self.evaluate_fitness()
        gene_index = random.randint(0, self.length - 1)
        gene = self.genes[gene_index]
        gene_binary = list(f'{gene:08b}')
        bit_index = random.randint(0, 7)
        gene_binary[bit_index] = '0' if gene_binary[bit_index] == '1' else '1'
        self.genes[gene_index] = int(''.join(gene_binary), 2)
        end_fit = self.evaluate_fitness()
        return start_fit, end_fit, gene_index

    def crossover(self, parent2):
        point = random.randint(1, self.length - 1)
        child = Individual(self.tasks, self.proc_num)
        child.genes = self.genes[:point] + parent2.genes[point:]
        return child, point


def create_logs(message):
    with open('genetic_algorithm_log.txt', 'a') as log_file:
        log_file.write(message + "\n")


class GeneticAlgorithm:
    def __init__(self, num_processors, num_tasks, x1, x2, population_size, max_repeats, crossover_prob, mutation_prob):
        self.num_processors = num_processors
        self.num_tasks = num_tasks
        self.task_times = [random.randint(x1, x2) for _ in range(num_tasks)]
        self.population_size = population_size
        self.max_repeats = max_repeats
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.population = [Individual(self.task_times, num_processors) for _ in range(population_size)]

        for item in self.population:
            item.initial()

        self.best_individual = None
        self.best_fitness = float('inf')
        self.repeats = 1
        self.iteration = 1
        self.logs_cross = ''
        self.logs_mutated = ''

    def run(self):
        create_logs(f"Tasks = {self.task_times}\n")
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

    def evaluate_population(self):
        population_fitness = []
        for item in self.population:
            item_fitness = item.evaluate_fitness()
            population_fitness.append(item_fitness)

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
            parent21_id = random.randint(0, self.population_size - 1)
            parent22_id = random.randint(0, self.population_size - 1)
            if (parent21_id == parent1_id) or (parent21_id == parent22_id) or (parent22_id == parent1_id):
                generate_random_parents_2(parent1_id)
            return parent21_id, parent22_id

        for item in self.population:
            self.logs_cross = ''
            self.logs_mutated = ''

            new_individual = copy.deepcopy(item)
            ind1 = str(self.population.index(item) + 1)

            trigger = random.random()
            if trigger < self.crossover_prob:

                # Модификация
                parent21, parent22 = generate_random_parents_2(int(ind1))

                if self.population[parent22].fitness < self.population[parent21].fitness:
                    new_individual, point = Individual.crossover(item, self.population[parent22])
                    ind2 = str(parent22 + 1)
                    self.logs_cross += f"Crossover {self.iteration - 1}/{ind1} X {self.iteration - 1}/{ind2} - Point {point}"
                else:
                    new_individual, point = Individual.crossover(item, self.population[parent21])
                    ind2 = str(parent21 + 1)
                    self.logs_cross += f"Crossover {self.iteration - 1}/{ind1} X {self.iteration - 1}/{ind2} - Point {point}"

            trigger = random.random()
            if trigger < self.mutation_prob:
                start_fit, end_fit, changed_ind = map(str, new_individual.mutate())
                self.logs_mutated += f"Obj {ind1} mutated on {changed_ind} chromosome ---> Fitness changed from {start_fit} to {end_fit}"

            if item.evaluate_fitness() < new_individual.evaluate_fitness():
                new_population.append(item)
            else:
                new_population.append(new_individual)

            if self.logs_cross != '':
                create_logs(self.logs_mutated)

        self.population = new_population
