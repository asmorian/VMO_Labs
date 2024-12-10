import re


def load_rules(filename):
    rules = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            lexeme, pattern = line.split(";", 1)
            rules[lexeme.strip()] = pattern.strip()
    return rules


class Lexer:
    def __init__(self, rules_file):
        self.rules = load_rules(rules_file)
        self.token_patterns = self.compile_patterns()

    def compile_patterns(self):
        token_patterns = []
        for lexeme, pattern in self.rules.items():
            regex = "|".join(re.escape(word) for word in re.findall(r"«(.*?)»", pattern))
            if not regex:
                regex = pattern
            token_patterns.append((lexeme, regex))
        return token_patterns

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = None
            for lexeme, regex in self.token_patterns:
                pattern = re.compile(rf"\A{regex}")
                match = pattern.match(text[position:])
                if match:
                    value = match.group(0)
                    tokens.append((lexeme, value))
                    position += len(value)
                    break
            if not match:
                raise ValueError(f"Неизвестная лексема в позиции {position}: '{text[position]}'")
            while position < len(text) and text[position].isspace():
                position += 1
        return tokens


if __name__ == "__main__":
    lexer = Lexer("rules.txt")
    text = "check F eq abc"

    try:
        tokens = lexer.tokenize(text)
        result = "".join(f"<{token[0]},{token[1]}>" for token in tokens)
        print(result)
    except ValueError as e:
        print(f"Ошибка: {e}")
