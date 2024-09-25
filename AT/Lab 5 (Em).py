import pandas as pd

# Исходная матрица Q
Q = pd.DataFrame({'a': [[], ['q2', 'q1'], []],
                  'b': [['q2'], ['q1'], []],
                  'e': [['q1'], [], ['q1']]},
                 index=['q0', 'q1', 'q2'])

# Словарь значений для каждого S
S_dict = {'S0': ['q0', 'q1'], 'S1': ['q1'], 'S2': ['q2', 'q1']}

# Функция для заполнения матрицы S
def fill_S(Q, S_dict):
    S = pd.DataFrame(index=S_dict.keys(), columns=Q.columns)

    for S_key, S_values in S_dict.items():
        for column in Q.columns:
            targets = set()
            for q in S_values:
                targets.update(Q.loc[q, column])

            for target in targets:
                for S_key_inner, S_values_inner in S_dict.items():
                    if target in S_values_inner:
                        S.loc[S_key, column] = S_key_inner

    return S

# Заполнение матрицы S
S = fill_S(Q, S_dict)

print(S)
