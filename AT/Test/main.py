from grammar import Grammar, context_sensitive

grammar = Grammar()
grammar.T = set(input('Введите терминальные символы: ').split(' '))
grammar.N = set(input('Введите нетерминальные символы: ').split(' '))
grammar.S = input('Введите начальный символ: ')

while (input_str := input('Введите правила: ')) != '':
    alpha, beta_unformatted = input_str.split(' -> ')
    grammar.add_rules(alpha, beta_unformatted.split(' | '))

# grammar.T = set('ab')
# grammar.N = set('SAB')
# grammar.S = 'S'
# grammar.P = {
#     'S': set(['aA']),
#     'A': set(['bB']),
#     # 'B': set(['c']),
#     'B': set(['b'])
# }

grammar.normalize()


print(grammar)
# print(context_sensitive('BC', 'BA', grammar.T, grammar.N))
print(grammar.get_type())
