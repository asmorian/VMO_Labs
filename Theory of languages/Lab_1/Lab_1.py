import re

# Класс автомата
class FiniteAutomaton:
    def __init__(self):
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    # Метод добавления перехода
    def add_transition(self, current, input_char, next_state):
        if current not in self.transitions:
            self.transitions[current] = {}
        self.transitions[current][input_char] = next_state

    # Метод задания начального состояния
    def set_start_state(self, state):
        self.start_state = state

    # Метод задания конечного состояния
    def add_final_state(self, state):
        self.final_states.add(state)

    # Метод проверки на соответствие
    def accepts(self, input_string):
        if self.start_state is None:
            raise ValueError("Start state is not defined.")
        current_state = self.start_state
        for char in input_string:
            if current_state not in self.transitions or char not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.final_states


def load_automaton_from_file(filename):
    a = FiniteAutomaton()
    with open(filename, 'r') as file:
        print("\n>> Введённые значения << \n")
        for line in file:
            match = re.match(r'^(q\d+);(.);(q\d+)$', line.strip())
            if not match:
                raise ValueError(f"Invalid transition format: {line}")
            current, input_char, next_state = match.groups()
            print(f"{current} -- {input_char} --> {next_state}")
            a.add_transition(current, input_char, next_state)
    return a


if __name__ == "__main__":
    automaton = load_automaton_from_file("transitions.txt")

    automaton.set_start_state("q0")
    automaton.add_final_state("q9")

    print("\n>> Переходы << \n")
    for item in automaton.transitions:
        print(f"Состояние: {item} \t Переходы: {automaton.transitions[item]}")
    print("")

    test_strings = ["if(0;T;F)", "if(1;T;F)", "if(2;T;F)", "if(1;F;T)"]
    for string in test_strings:
        result = automaton.accepts(string)
        print(f"String '{string}' is {'accepted' if result else 'rejected'}.")
