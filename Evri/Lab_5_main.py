import Lab_5_func as lp

N = 3  # количество процессоров
M = 11  # количество заданий
x1 = 10  # нижний предел времени выполнения задания
x2 = 20  # верхний предел времени выполнения задания
Z = 10  # количество особей в поколении
Y = 10  # количество повторений для остановки
Pn = 0.7  # вероятность кроссовера
Pm = 0.7  # вероятность мутации

with open('genetic_algorithm_log.txt', 'w'):
    pass
ga = lp.GeneticAlgorithm(N, M, x1, x2, Z, Y, Pn, Pm)
ga.run()
print(f"Tasks: {ga.task_times}")
print(f"Best Solution: {ga.best_individual.genes} with Fitness: {ga.best_individual.fitness}")

# test = lp.Individual([13, 15, 15, 15, 12, 1, 16, 4, 8, 9], 3)
# test.genes = [209, 118, 189, 19, 232, 181, 97, 9, 31, 33]
# print(test.evaluate_fitness())
