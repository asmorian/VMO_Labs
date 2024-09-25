from gram import Grammar


def set_T():
    T = []
    while True:
        input_string = input("Введите терминальные символы (T): ")
        if input_string:
            filtered_string = ''.join(filter(lambda x: x.isalnum(), input_string))
            for char in filtered_string:
                if char not in T:
                    T.append(char)
            return T
        else:
            print("Должен существовать как минимум один терминальный символ!")
            continue


def set_N():
    N = []
    while True:
        input_string = input("Введите нетерминальные символы (N): ")
        if input_string:
            filtered_string = ''.join(filter(str.isalpha, input_string.upper()))
            for char in filtered_string:
                if char not in N:
                    N.append(char)
            if "S" not in N:
                N.append("S")
            return N
        else:
            print("Должен существовать как минимум один нетерминальный символ S")
            continue


def set_P(N):
    P = {}
    for item in N:
        P[item] = (input(f"Правило {item} -> "))
    return P


def set_all():
    T = set_T()
    N = set_N()
    S = "S"
    P = set_P(N)

    print(f"Т = {T}\n",
          f"N = {N}\n",
          f"S = S\n",
          f"P = {P}", sep="")

    return T, N, S, P


# T, N, S, P = set_all()
# G2 = Grammar(T, N, S, P)
G = Grammar(['a', 'b', 'c'], ['S', 'B', 'C'], "S", {'S': 'ab', 'B': 'bC', 'C': 'c'})
G2 = Grammar(['a', 'b', 'c'], ['S', 'aB', 'C'], "S", {'S': 'aBbC', 'aB': 'a | Ba', 'C': 'cc'})
G3 = Grammar(['a', 'b'], ['S', 'B'], "S", {'S': 'aBS | e', 'aB': 'ab'})

G.show()
G.get_type()
print("====================")
G2.show()
G2.get_type()
print("====================")
G3.show()
G3.get_type()
