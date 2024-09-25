import pandas as pd


class TransitionMatrix:
    def __init__(self, alphabet, numOfVert, initialStates, finalStates):
        self.alphabet = alphabet
        self.numOfVert = numOfVert
        self.initialStates = initialStates
        self.finalStates = finalStates
        self.S = []
        self.S_dict = {}
        self.P_dict = {}
        self.s_matrix = pd.DataFrame()
        self.p_matrix = pd.DataFrame()

        data = [[[] for _ in range(len(numOfVert))] for _ in range(len(alphabet))]
        self.t_matrix = pd.DataFrame(data, index=alphabet, columns=numOfVert)

    def getTabel(self):
        print(self.t_matrix.T)
        print("Входные состояния:", self.initialStates,
              "\nФинальные состояния", self.finalStates)
        print("------------------------------------------")

    def setTabelWay(self, string_way):
        way = string_way.split(" ")
        self.t_matrix.loc[way[1], way[0]].append(way[2])

    def creating_S(self):
        for _ in range(len(self.numOfVert)):
            self.S.append([self.numOfVert[_]])
            for way in self.t_matrix.loc["e", self.numOfVert[_]]:
                self.S[_].append(way)

        for i, s_values in enumerate(self.S):
            key = f'S{i}'
            self.S_dict[key] = s_values
        return self.S_dict

    def print_S(self):
        if self.S_dict["S0"]:
            for i in range(len(self.S)):
                print(f"S{i} = ", self.S_dict[f"S{i}"])
        print("------------------------------------------")

    def inner_final_S(self):
        inner_s = []
        final_s = []
        for item in self.S_dict["S0"]:
            inner_s.append(f"S{item[1:]}")
        for item in self.finalStates:
            final_s.append(f"S{item[1:]}")
        return inner_s, final_s

    def creatingMatrix_S(self):
        data = [[[] for _ in range(len(self.S))] for _ in range(len(self.alphabet) - 1)]
        columnsName = []
        s_alphabet = self.alphabet[0:len(self.alphabet) - 1]
        for _ in range(len(self.S)):
            columnsName.append(f"S{_}")
        self.s_matrix = pd.DataFrame(data, index=s_alphabet, columns=columnsName)
        self.s_matrix = self.s_matrix.T

        for column_name, series in self.s_matrix.iterrows():
            for index, item in series.items():
                for vert in self.S_dict[column_name]:
                    if self.t_matrix[vert][index]:
                        if self.t_matrix[vert][index] not in item:
                            item.append(self.t_matrix[vert][index])
                        for i in self.t_matrix[vert][index]:
                            if self.t_matrix[i]["e"] and self.t_matrix[i]["e"] not in item:
                                item.append(self.t_matrix[i]["e"])
                    if self.t_matrix[vert]["e"]:
                        for e_vert in self.t_matrix[vert]["e"]:
                            if self.t_matrix[e_vert][index] and self.t_matrix[e_vert][index] not in item:
                                item.append(self.t_matrix[e_vert][index])

        for column_name, series in self.s_matrix.iterrows():
            for index, item in series.items():
                new_item = flatten_and_sort(item)
                for i in range(len(new_item)):
                    new_item[i] = f"S{new_item[i][1:]}"
                self.s_matrix[index][column_name] = new_item

        print(self.s_matrix)

        inner, final = self.inner_final_S()
        print("Входные состояния:", inner,
              "\nФинальные состояния:", final)
        print("------------------------------------------")

    def bind_P(self):
        P = []
        inner_s, final_s = self.inner_final_S()
        P.append(inner_s)
        for way in self.alphabet[:(len(self.alphabet) - 1)]:
            temp = []
            for item in P[0]:
                temp.append(self.s_matrix[way][item])
                temp = flatten_and_sort(temp)
            P.append(temp)
        self.P_dict = list_to_dict(P)

    def creatingMatrix_P(self):
        data = [[[] for _ in range(len(self.P_dict))] for _ in range(len(self.alphabet) - 1)]
        columnsName = []
        p_alphabet = self.alphabet[0:len(self.alphabet) - 1]
        for _ in self.P_dict:
            columnsName.append(_)
        self.p_matrix = pd.DataFrame(data, index=p_alphabet, columns=columnsName)
        self.p_matrix = self.p_matrix.T
        self.s_matrix = self.s_matrix.T

        for column_name, series in self.p_matrix.iterrows():
            for index, item in series.items():
                for vert in self.P_dict[column_name]:
                    if self.s_matrix[vert][index]:
                        if self.s_matrix[vert][index] not in item:
                            item.append(self.s_matrix[vert][index])

        for column_name, series in self.p_matrix.iterrows():
            for index, item in series.items():
                self.p_matrix[index][column_name] = flatten_and_sort(self.p_matrix[index][column_name])
        print(self.p_matrix)
        print("------------------------------------------")

        for column_name, series in self.p_matrix.iterrows():
            for index, item in series.items():
                if get_index_by_value(self.P_dict, item):
                    self.p_matrix[index][column_name] = get_index_by_value(self.P_dict, item)
                else:
                    self.p_matrix[index][column_name] = "Ø"

        inner_s, final_s = self.inner_final_S()
        final_p = []
        for item in self.P_dict:
            if final_s[0] in self.P_dict[item]:
                final_p.append(item)

        print(self.p_matrix)
        print("Входные состояния:", ["P0"],
              "\nФинальные состояния:", final_p)
        print("------------------------------------------")

    def determ(self):
        self.getTabel()
        self.creating_S()
        self.print_S()
        self.creatingMatrix_S()
        self.bind_P()
        self.creatingMatrix_P()


def get_index_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def flatten_and_sort(K):
    flattened = []

    # Функция для рекурсивного обхода вложенных списков
    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                flatten(item)
            else:
                flattened.append(item)

    flatten(K)
    unique_sorted = sorted(set(flattened))
    return unique_sorted


def list_to_dict(lst):
    return {f'P{i}': sublist for i, sublist in enumerate(lst)}


trigger = 1
while trigger != "0":
    trigger = input("1 - Ввести граф от руки\n2 - Ввести граф автоматически\n---> ")
    if trigger == "1":
        alph = input("Введите алфавит через пробел (Например: a b c e) ---> ").split(" ")
        vert = input("Введите вершины (Например: q0 q1 q2) ---> ").split(" ")
        inner = input("Введите входные вершины ---> ").split(" ")
        final = input("Введите финальные вершины ---> ").split(" ")
        db = TransitionMatrix(alph, vert, inner, final)
        db.getTabel()
        print("Введите путь в формате (q0 a q1), либо 0 чтобы завершить заполнение")
        while trigger != "0":
            trigger = input("---> ")
            if trigger != "0":
                db.setTabelWay(trigger)
                db.getTabel()
        db.determ()

    else:
        db = TransitionMatrix(['a', 'b', 'e'], ['q0', 'q1', 'q2'], ["q0"], ["q2"])
        db.setTabelWay("q0 b q2")
        db.setTabelWay("q0 e q1")
        db.setTabelWay("q1 b q1")
        db.setTabelWay("q1 a q2")
        db.setTabelWay("q1 a q0")
        db.setTabelWay("q2 e q1")
        db.getTabel()
        db.determ()
        trigger = "0"
