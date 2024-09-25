EPSILON = 'ε'

def get_eps_list(non_eps: list[str]) -> list[str]:
    return [(x == '' and 'ε' or x) for x in non_eps]

def get_union_start(s_1: str, s_2: str) -> str:
    union_start = ''
    cur_i = 0

    s_1_len = len(s_1)
    s_2_len = len(s_2)

    while s_1[cur_i] == s_2[cur_i]:
        union_start += s_1[cur_i]
        cur_i += 1
        if cur_i >= s_1_len or cur_i >= s_2_len:
            return union_start
    
    return union_start


def context_sensitive(alpha: str, beta: str, T: set[str], N: set[str]) -> bool:
    xi_1 = get_union_start(alpha, beta)
    xi_2 = get_union_start(alpha[::-1], beta[::-1])
    
    # отрезаем левые части
    if len(xi_1) > 0:
        alpha = alpha[len(xi_1):]
        beta = beta[len(xi_1):]

    # отрезаем правые части
    if len(xi_2) > 0:
        alpha = alpha[::-1][len(xi_2)-1:][::-1]
        beta = beta[::-1][len(xi_2)-1:][::-1]

    if len(alpha) > 1 or alpha in T:
        return False

    if len(beta) == 0:
        return False
    
    return True


class Grammar:
    def __init__(self):
        self.T: set[str] = set()
        self.N: set[str] = set()
        self.P: dict[str, set[str]] = {}
        self.S: str = ''

    def format_p(self):
        lines = []

        for alpha in self.P:
            lines.append('%s -> %s\n' % (alpha, ' | '.join(get_eps_list(self.P[alpha]))))

        return '\t'.join(lines)

    def normalize(self):
        self.T.add('')
    
    def add_rules(self, alpha, betas):
        # a = [(x == 'eps' and '' or x) for x in betas]
        betas_fixed = set()
        for beta in betas:
            if beta == 'eps':
                betas_fixed.add('')
            else:
                betas_fixed.add(beta)
        self.P[alpha] = betas_fixed

    def get_type_3(self):
        is_left, is_right = True, True
        for alpha in self.P:
            # с левой стороны должен быть один символ
            if len(alpha) > 1:
                return -1
            # если левый символ содержится в терминальных
            if alpha in self.T:
                return -1
            betas = self.P[alpha]
            for beta in betas:
                if beta == '':
                    return -1
                # случай wB
                if beta[-1] in self.N:
                    # удаляем из рассмотрения
                    beta = beta[:-1]
                    # это точно не левостороннее
                    is_left = False
                # случай Bw
                elif beta[0] in self.N:
                    beta = beta[1:]
                    is_right = False
                # если хотя бы один символ из w содержится в нетерминальных, то это плохо
                if len(set(beta) & self.N) > 0:
                    return -1
            
            # исключение - это 2 тип
            # if is_right and is_left:
            #     return -1
            # elif is_left:
        if is_left:
            return 1
        elif is_right:
            return 2
        else:
            return -1
    
    def get_type_2(self):
        for alpha in self.P:
            if len(alpha) > 1:
                return -1
            if alpha in self.T:
                return -1
        return 1

    def get_type_1(self):
        is_growing = True
        is_context_sensitive = True
        for alpha in self.P:
            for beta in self.P[alpha]:
                # неукорачивающая
                if len(alpha) > len(beta):
                    is_growing = False
                # кз
                if not context_sensitive(alpha, beta, self.T, self.N):
                    is_context_sensitive = False

        if is_growing and is_context_sensitive:
            return 3
        elif is_growing:
            return 2
        elif is_context_sensitive:
            return 1
        else: 
            return -1

    def get_type(self):
        if (type3 := self.get_type_3()) != -1:
            return 'Тип 3, ' + (type3 == 1 and 'леволинейный' or 'праволинейный')
        elif self.get_type_2() != -1:
            return 'Тип 2 (контекстно-свободный)'
        elif (type1 := self.get_type_1()) != -1:
            if type1 == 3:
                return 'Тип 1. Неукорачивающий, контекстно-зависимый'
            elif type1 == 2:
                return 'Тип 1. Неукорачивающий'
            else:
                return 'Тип 1. Контекстно-зависимый'
        return 'Тип 0'

    def __str__(self):
        return 'G<{%s}, {%s}, P, %s>\nP:\n\t%s' % (
            ', '.join(map(lambda x: x == '' and 'ε' or x, self.T)),
            ', '.join(self.N),
            self.S, self.format_p())