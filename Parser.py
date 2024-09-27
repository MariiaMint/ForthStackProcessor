from typing import List, Union, Optional
from Lexer import Token

class ASTNode:
    def pretty_print(self, level=0):
        raise NotImplementedError

class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}NumberNode({self.value})")

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value.strip('"')

    def __repr__(self):
        return f"StringNode({self.value})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}StringNode({self.value})")

class OperationNode(ASTNode):
    def __init__(self, operator: str, numbers: list):
        self.operator = operator
        self.numbers = numbers

    def __repr__(self):
        return f"OperationNode('{self.operator}')"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}OperationNode('{self.operator}')")
        for node in self.numbers:
            if node:
                node.pretty_print(level + 2)

class NameNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"NameNode({self.value})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}NameNode({self.value})")

class FunctionNode(ASTNode):
    def __init__(self, name: str, enter_data: list, return_data: list, body: list):
        self.name = name
        self.enter_data = enter_data
        self.return_data = return_data
        self.body = body

    def __repr__(self):
        return f"FunctionNode('{self.name}', {self.body})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}FunctionNode('{self.name}':")

        print(f"{indent}  Enter Data:")
        for node in self.enter_data:
            if node:
                node.pretty_print(level + 2)

        print(f"{indent}  Return Data:")
        for node in self.return_data:
            if node:
                node.pretty_print(level + 2)
        
        print(f"{indent}  Body:")
        for node in self.body:
            if node:
                node.pretty_print(level + 2)
        print(f"{indent})")

class FunctionCallNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"FunctionCallNode({self.name})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}FunctionCallNode({self.name})")

class SignNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"SignNode('{self.value}')"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}SignNode('{self.value}')")


class CompareNode(ASTNode):
    def __init__(self, sign: SignNode, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
        self.sign = sign

    def __repr__(self):
        return f"CompareNode({self.sign}, {self.left}, {self.right})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}CompareNode:")
        print(f"{indent}  Sign:")
        self.sign.pretty_print(level + 2)
        print(f"{indent}  Left:")
        self.left.pretty_print(level + 2)
        print(f"{indent}  Right:")
        self.right.pretty_print(level + 2)

class ConditionalNode(ASTNode):
    def __init__(self, condition: CompareNode, true_branch: list, false_branch: list):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"ConditionalNode({self.condition}, {self.true_branch}, {self.false_branch})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}ConditionalNode:")
        if self.condition:
            print(f"{indent}  Condition:")
            self.condition.pretty_print(level + 2)
        print(f"{indent}  True Branch:")
        for node in self.true_branch:
            if node:
                node.pretty_print(level + 2)
        if self.false_branch:
            print(f"{indent}  False Branch:")
            for node in self.false_branch:
                if node:
                    node.pretty_print(level + 2)

class LoopNode(ASTNode):
    def __init__(self, end: NameNode, start: NameNode, body: list):
        self.start = start
        self.end = end
        self.body = body

    def __repr__(self):
        return f"LoopNode({self.start}, {self.end}, {self.body})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}LoopNode:")
        if self.start:
            print(f"{indent}  Start:")
            self.start.pretty_print(level + 2)
        if self.end:
            print(f"{indent}  End:")
            self.end.pretty_print(level + 2)
        print(f"{indent}  Body:")
        for node in self.body:
            if node:
                node.pretty_print(level + 2)

class InputNode(ASTNode):

    def __repr__(self):
        return f"InputNode('')"

    def pretty_print(self, level=0):
        indent = '  ' * level
        print(f"{indent}InputNode()")

class OutputNode(ASTNode):
    def __init__(self, optional: ASTNode):
        self.optional = optional

    def __repr__(self):
        return f"OutputNode({self.optional})"

    def pretty_print(self, level=0):
        indent = '  ' * level
        if isinstance(self.optional, StringNode):
            print(f"{indent}Output string:")
            self.optional.pretty_print(level + 2)
        elif isinstance(self.optional, FunctionCallNode):
            print(f"{indent}Output name:")
            self.optional.pretty_print(level + 2)
        else:
            print(f"{indent}OutputNode(stack_top)")

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.stack = []

    def parse(self) -> list:
        nodes = []
        while self.pos < len(self.tokens):
            node = self.parse_statement()
            if node and not(isinstance(node, NumberNode)) and not(isinstance(node, StringNode)) and not(isinstance(node, NameNode)):
                nodes.append(node)
        return nodes

    def parse_statement(self) -> ASTNode:
        token = self.current_token()
        if token.type == 'START_FUNCTION':
            return self.parse_function()
        elif token.type == 'NUMBER':
            return self.parse_number()
        elif token.type == 'STRING':
            return self.parse_string()
        elif token.type == 'IF':
            return self.parse_conditional()
        elif token.type == 'DO':
            return self.parse_loop()
        elif token.type == 'OPERATION':
            return self.parse_operation()
        elif token.type == 'COMPARE':
            return self.parse_compare()
        elif token.type == 'INPUT':
            return self.parse_input()
        elif token.type == 'NAME':
            return self.parse_name()
        elif token.type == 'OUTPUT':
            return self.parse_output()
        else:
            self.pos += 1
            return None

    def parse_function(self) -> FunctionNode:
        self.consume('START_FUNCTION')
        name_token = self.consume('NAME')
        enter_data = []
        self.consume('LPAREN')

        while not self.match('SEPARATOR'):
            data = self.parse_statement()
            if data:
                enter_data.append(data)
        self.consume('SEPARATOR')
        for i in range(len(enter_data)):
            self.stack.pop()

        return_data = []

        while not self.match('RPAREN'):
            if self.match('LPAREN'):
                self.consume('LPAREN')
                while not self.match('RPAREN'):
                    data = self.parse_statement()
                    
                self.consume('RPAREN')
            else: data = self.parse_statement()
            if data:
                return_data.append(data)
        
        self.consume('RPAREN')
        for i in range(len(return_data)):
            self.stack.pop()
            
        body = []

        while not self.match('END_FUNCTION'):
            node = self.parse_statement()
            if node:
                if (isinstance(node, CompareNode) or isinstance(node, LoopNode) ):
                    body.pop(-1)
                    body.pop(-1)
                elif (isinstance(node, ConditionalNode)):
                    body.pop(-1)
                
                # print("body", node)
                body.append(node)
        self.consume('END_FUNCTION')
        return FunctionNode(name_token.value, enter_data, return_data, body)

    def parse_number(self) -> NumberNode:
        token = self.consume('NUMBER')
        node = NumberNode(float(token.value))
        self.stack.append(node)
        return node
    
    def parse_output(self) -> OutputNode:
        self.consume('OUTPUT')  
        node = self.parse_statement()  
        if isinstance(node, StringNode) or isinstance(node, FunctionCallNode):
            if not isinstance(node, FunctionCallNode):
                self.consume('END_FUNCTION')  
            return OutputNode(node)
        
        return OutputNode(None)  

    def parse_string(self) -> StringNode:
        token = self.consume('STRING')
        self.stack.append(StringNode(token.value))
        return StringNode(token.value)
    
    def parse_operation(self) -> OperationNode:
        while not self.match('END_FUNCTION'):
            operator = self.consume('OPERATION')
            numbers = [self.stack.pop(), self.stack.pop()]
            operation = OperationNode(operator.value, numbers)
            self.stack.append(operation)
            node = self.parse_statement()
            if node is None:
                return operation
       
    def parse_conditional(self) -> ConditionalNode:
        self.consume('IF')
        condition = self.stack.pop()
        true_branch = []
        while not self.match('ELSE', 'FINISH'):
            node = self.parse_statement()
            if node:
                true_branch.append(node)
        if self.match('ELSE'):
            self.consume('ELSE')
            false_branch = []
            while not self.match('FINISH'):
                node = self.parse_statement()
                if node:
                    false_branch.append(node)
            self.consume('FINISH')
            return ConditionalNode(condition, true_branch, false_branch)
        else:
            self.consume('FINISH')
            return ConditionalNode(condition, true_branch, [])

    def parse_loop(self) -> LoopNode:
        self.consume('DO')
        start = self.stack.pop()
        end = self.stack.pop()
        body = []
        while not self.match('LOOP'):
            # print("body", body)
            # print(self.tokens[self.pos])
            node = self.parse_statement()
            # print(node)
            if node:
                if (isinstance(node, CompareNode) or isinstance(node, LoopNode) or isinstance(node, OperationNode) ):
                    body.pop(-1)
                    body.pop(-1)
                elif (isinstance(node, ConditionalNode)):
                    body.pop(-1)

                body.append(node)
            if self.pos >= len(self.tokens):
                raise SyntaxError("Unexpected end of tokens inside loop construct")
        self.consume('LOOP')
        return LoopNode(end, start, body)

    def parse_compare(self) -> CompareNode:
        token = self.consume('COMPARE')
        sign = SignNode(token.value)  # создаем узел для знака
        left = self.stack.pop()
        right = self.stack.pop()
        node = CompareNode(sign, left, right)
        self.stack.append(node)
        return node


    def parse_input(self) -> InputNode:
        self.consume('INPUT')
        node = InputNode()
        self.stack.append(node)
        return node
    
    def parse_name(self) -> Union[NameNode, FunctionCallNode]:
        token = self.consume('NAME')
        # Проверяем, если следующим токеном идет END_FUNCTION
        if self.match('END_FUNCTION'):
            self.consume('END_FUNCTION')
            return FunctionCallNode(token.value)
        else:
            node = NameNode(token.value)
            self.stack.append(node)
            return node


    def consume(self, token_type: str):
        token = self.current_token()
        if token.type == token_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected token {token_type}, got {token.type}")

    def match(self, *token_types: str) -> bool:
        if self.pos >= len(self.tokens):
            return False
        return self.current_token().type in token_types

    def current_token(self):
        if self.pos >= len(self.tokens):
            raise IndexError("Attempted to access token beyond the end of the list.")
        return self.tokens[self.pos]
