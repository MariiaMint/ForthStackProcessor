import re
from typing import List

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self):
        self.token_specification = [
            ('COMMENT',  r'^\\.*'),           # Single line comments starting with "\"
            ('START_FUNCTION', r':'),        #Starts with : then a space and any letters before another space
            ('SEPARATOR',  r'-{2}'),
            ('OPERATION',r'[+\-*\/]{1}'),   # Space and any of +-*/
            ('COMPARE',  r'={2}|>|<'),
            ('NUMBER',   r'\d+'),             # Integer values          
            ('OUTPUT',   r'\.'),
            ('END_FUNCTION',   r';'),
            ('DO',       r'DO'),              # Loop start
            ('LOOP',     r'LOOP'),            # Loop end
            ('IF',       r'IF'),              # If condition start
            ('ELSE',     r'ELSE'),            # Else condition
            ('FINISH',   r'FINISH'),          # Finish conditionals or branches
            ('STRING',  r'\" .+?\"'),         # String quote indicator
            ('INPUT',    r'INPUT'),           # Input operation
            ('NAME', r'[A-Za-z][A-Za-z0-9\-]*'),
            ('LPAREN',   r'\('),              # Left parenthesis
            ('RPAREN',   r'\)'),              # Right parenthesis
            ('SKIP',     r'[ \t\n]+'),        # Skip spaces, tabs, and newlines
            ('MISMATCH', r'.'),               # Any other character (mismatched)
        ]
        self.tokens_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification)

    def tokenize(self, code: List) -> List[Token]:
        tokens = []
        for line in code:
            for match in re.finditer(self.tokens_regex, line):
                type_ = match.lastgroup
                value = match.group(type_)
                if type_ == 'SKIP' or type_ == 'COMMENT':
                    continue
                if type_ == 'MISMATCH':
                    raise RuntimeError(f'Unexpected character "{value}"')
                tokens.append(Token(type_, value))
                print(Token(type_, value))
        return tokens
