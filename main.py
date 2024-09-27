from Lexer import Lexer
from Parser import Parser
from AssmGen import AssmGen
from AssmToJson import AssmToJson
import json

if __name__ == "__main__":
    with open("cat.frth", encoding="utf-8") as file:
        code = file.readlines()

    lexer = Lexer()
    tokens = lexer.tokenize(code)

    # for token in tokens:
    #     print(token)

    parser = Parser(tokens)
    ast = parser.parse()
    # Печать AST в виде дерева
    for node in ast:
        if node:
            node.pretty_print()
            print()

    assm_gen = AssmGen()
    asm_code = assm_gen.generate(ast)
    print(asm_code)

    converter = AssmToJson(asm_code)
    json_output = converter.convert()
    converter.save_to_file('output.json')
