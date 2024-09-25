class Grammar:
    def __init__(self, T, N, S, P):
        self.T = T
        self.N = N
        self.S = S
        self.P = P

    def show(self):
        print(f"Т = {self.T}\n",
              f"N = {self.N}\n",
              f"S = S", sep="")
        print("P = {")
        for item in self.P:
            print(f"{item} -> {self.P[item]}")
        print("}")

    def checker(self, word):
        check = True
        for item in self.N:
            if item in word:
                check = False
        return check

    def get(self, numOfIter):
        final_string = self.P[self.S]
        temp_mass = []
        for item in final_string:
            temp_mass.append(item)
        for i in range(numOfIter):
            for j in range(len(temp_mass)):
                if temp_mass[j] in self.P:
                    temp = temp_mass[j]
                    temp_mass[j] = self.P[temp]
            result = [char for string in temp_mass for char in string]
            temp_mass = result
            final_mass = [char for char in temp_mass if char not in self.P]
            final_string = ''.join(final_mass)
            print(final_string)
        print("-" * len(final_string))

    def type_1(self):
        # Проверка на неукор.
        non_shortable = []
        for item in self.P:
            for word in self.P[item].split(" | "):
                if len(item) > len(word):
                    non_shortable.append(False)
                else:
                    non_shortable.append(True)

        # Контекстно-зависимые
        context_sens = []
        for item in self.P:
            temp = False
            for letter in item:
                if letter in self.N:
                    temp = True
            context_sens.append(temp)

        return non_shortable, context_sens

    def type_2(self):
        # Контекстно-независимые
        context_free = []
        for item in self.P:
            if "|" in self.P[item]:
                p_items = self.P[item].split(" | ")
                is_context_free = True
                for i in range(len(p_items)):
                    if len(item) < len(p_items[i]):
                        is_context_free = False
                context_free.append(is_context_free)
            if item in self.N:
                context_free.append(True)
            else:
                context_free.append(False)

        return context_free

    def type_3(self):
        # Регулярная
        regular_r = []
        regular_l = []
        rr = False
        rl = False

        for item in self.P:
            for i in range(len(self.P[item])):
                if (self.P[item][i] in self.N and i > 0 and i + 1 >= len(self.P[item])) or self.checker(self.P[item]):
                    rr = True
                else:
                    rr = False
            regular_r.append(rr)
            for j in range(len(self.P[item])):
                if (self.P[item][j] in self.N and j == 0 and len(self.P[item]) > 1) or self.checker(self.P[item]):
                    rl = True
                    break
                else:
                    rl = False
            regular_l.append(rl)

        return regular_r, regular_l

    def get_type(self):
        non_shortable, context_sens = self.type_1()
        context_free = self.type_2()
        regular_r, regular_l = self.type_3()

        gram_type = "Check!"
        if False in non_shortable and False in context_sens:
            gram_type = "Тип 0"
        elif False in non_shortable and not (False in context_sens):
            gram_type = "Тип 1 - Контекстно-зависимый"
        elif False in context_sens and not (False in non_shortable):
            gram_type = "Тип 1 - Не укорачивающий"
        elif not (False in context_sens) and not (False in non_shortable):
            gram_type = "Тип 1 - Не укорачивающий и контекстно зависимый"

            if not (False in context_free):
                gram_type = "Тип 2 - Контекстно-независимый"
                if not (False in regular_l):
                    gram_type = "Тип 3 - Левосторонний"
                if not (False in regular_r):
                    gram_type = "Тип 3 - Правосторонний"

        print(gram_type)
