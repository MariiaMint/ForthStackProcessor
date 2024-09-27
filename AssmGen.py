from typing import List
from Parser import ASTNode, NumberNode, StringNode, OperationNode, NameNode, FunctionNode, CompareNode, ConditionalNode, LoopNode, InputNode, OutputNode, FunctionCallNode

class AssmGen:
    def __init__(self):
        self.instructions = []
        self.label_count = 0
        self.variable_table = {}
        self.current_function = None
        self.function_names = []
        self.data_section = {}
        self.string_count = 0

    def generate(self, ast: List[ASTNode]) -> str:
        for data in self.data_section:
            self.instructions.append(data)

        for node in ast:
            self.visit(node)

        print("переменные и адреса ", self.variable_table) 
        print("адреса и данные", self.data_section)

        return "\n".join(self.instructions)

    def visit(self, node: ASTNode):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        result = visitor(node)
        if method_name == "visit_CompareNode":
            return result  # Возвращаем результат, если это visit_CompareNode
    
    def generic_visit(self, node: ASTNode):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def visit_NumberNode(self, node: NumberNode):
        self.instructions.append(f"PUSH {node.value}")

    def visit_StringNode(self, node: StringNode):
        string_label = f".string_{self.string_count}"
        string_data = f"{string_label}: .string \"{node.value}\\0\""
        self.data_section.append(string_data)
        self.variable_table[node.value] = string_label
        self.string_count += 1

    def visit_NameNode(self, node: NameNode):
        if node.value in self.variable_table:
            self.instructions.append(f"LOAD {self.variable_table[node.value]}")

    def visit_OperationNode(self, node: OperationNode):

        for n in range(len(node.numbers)-1, -1, -1):
            self.visit(node.numbers[n])
        if node.operator == "+":
            self.instructions.append(f"ADD")
        if node.operator == "-":
            self.instructions.append(f"SUB")
        if node.operator == "*":
            self.instructions.append(f"MUL")
        if node.operator == "/":
            self.instructions.append(f"DIV")

    def visit_FunctionNode(self, node: FunctionNode):
        self.function_names.append(node.name)
        self.current_function = node.name

        for return_node in node.return_data:
            if isinstance(return_node, NumberNode):
                if node.name not in self.variable_table:
                    self.variable_table[node.name] = len(self.data_section)
                    self.data_section[len(self.data_section)] = return_node.value
                else:
                    self.data_section[self.variable_table[node.name]] = return_node.value
                self.instructions.append(f"PUSH {return_node.value}")

                self.instructions.append(f"STORE {self.variable_table[node.name]}")

            elif isinstance(return_node, InputNode):
                self.variable_table["iter"] = len(self.data_section)
                self.data_section[self.variable_table["iter"]] = len(self.data_section)
                self.variable_table[node.name] = len(self.data_section)
                for i in range(25):
                    self.data_section[self.variable_table[node.name]+i] = 0
                
                start_label_1 = self.new_label()
                end_label = self.new_label()

                self.instructions.append(f"PUSH {self.data_section[self.variable_table["iter"]]}")
                self.instructions.append(f"STORE {self.variable_table["iter"]}")

                self.instructions.append(f"{start_label_1}:")
                

                self.instructions.append("IN")
                self.instructions.append("DUP")
                self.instructions.append("PUSH 0")
                self.instructions.append("CMP")
                self.instructions.append(f"JUMP_IF_EQUAL {end_label}")

                self.instructions.append(f"LOAD {self.variable_table["iter"] }")
                self.instructions.append(f"INC")
                self.instructions.append(f"STORE {self.variable_table["iter"] }")

                self.instructions.append(f"LOAD {self.variable_table["iter"] }")
                self.instructions.append(f"STORE_TOP")
                
                self.instructions.append(f"JUMP {start_label_1}")

                self.instructions.append(f"{end_label}:")
                self.instructions.append(f"PUSH 0")
                self.instructions.append(f"LOAD {self.variable_table["iter"] }")
                self.instructions.append(f"INC")
                self.instructions.append(f"STORE {self.variable_table["iter"] }")

                self.instructions.append(f"LOAD {self.variable_table["iter"] }")
                self.instructions.append(f"STORE_TOP")

                self.instructions.append(f"PUSH {self.data_section[self.variable_table["iter"]] }")
                self.instructions.append(f"INC")
                self.instructions.append(f"STORE {self.variable_table["iter"]}")

                self.instructions.append(f"RET")

            elif isinstance(return_node, StringNode):
                self.variable_table[node.name] = len(self.data_section)
                
                for i in range(len(return_node.value)-1):
                    ascii_code = ord(return_node.value[i+1])
                    self.data_section[len(self.data_section)] = ord(return_node.value[i])
                    
                    self.instructions.append(f"PUSH {ascii_code}")
                    self.instructions.append(f"STORE {self.variable_table[node.name] + i}")
                    
                self.data_section[len(self.data_section)] = 0 
                self.instructions.append(f"PUSH 0")
                self.instructions.append(f"STORE {self.variable_table[node.name] + i +1}")
                
            elif isinstance(return_node, NameNode):
                if node.name not in self.variable_table:
                    self.variable_table[node.name] = len(self.data_section)
                if return_node.value in self.variable_table:
                    if node.name not in self.variable_table:
                        self.data_section[len(self.data_section)] = self.data_section[self.variable_table[return_node.value]]
                    else:
                        self.data_section[self.variable_table[node.name]] = self.data_section[self.variable_table[return_node.value]]

                    self.instructions.append(f"LOAD {self.variable_table[return_node.value]}")

                    self.instructions.append(f"STORE {self.variable_table[node.name]}")


            elif isinstance(return_node, OperationNode):
                if node.name not in self.variable_table:
                    self.variable_table[node.name] = len(self.data_section)
                    self.data_section[self.variable_table[node.name]] = 0
                self.visit_OperationNode(return_node)
                self.instructions.append(f"PUSH {self.variable_table[node.name]}")
                self.instructions.append(f"STORE_TOP")

        self.instructions.append(f"{node.name}:")

        for i, entry in enumerate(node.enter_data):
            if isinstance(entry, InputNode):
                self.handle_input(entry)
            else:
                self.instructions.append("IN")
                self.variable_table[entry.value] = len(self.data_section) 
                self.data_section[len(self.data_section)] = f"value_{i}"
                self.instructions.append(f"STORE {self.variable_table[entry.value]}")

        for return_node in node.return_data:
            if isinstance(return_node, NumberNode) or isinstance(return_node, NameNode) or isinstance(return_node, OperationNode):
                self.instructions.append(f"LOAD {self.variable_table[node.name]}")

            elif isinstance(return_node, InputNode):
           
                self.instructions.append(f"PUSH {self.variable_table[node.name]}")

            elif isinstance(return_node, StringNode):
                self.instructions.append(f"PUSH {self.variable_table[node.name]}")

                

        for statement in node.body:
            self.visit(statement)

        self.instructions.append("RET")
        for return_node in node.return_data:
            if (isinstance(return_node, InputNode)):
                self.instructions.append(f"CALL {start_label_1}")
            self.current_function = None

    def visit_CompareNode(self, node: CompareNode):
        if isinstance(node.left, NameNode) and isinstance(node.right, NameNode):
            if node.left.value in self.variable_table and node.right.value in self.variable_table:
                left_address = self.variable_table[node.left.value]
                right_address = self.variable_table[node.right.value]
                self.compare_strings_in_memory(left_address, right_address)

        else:
            self.visit(node.left)
            self.visit(node.right)
            self.instructions.append("CMP")
        if node.sign.value == "==":
            return "JUMP_IF_FALSE"
        else :
            return "JUMP_IF_GREATER"

    def compare_strings_in_memory(self, left_addr, right_addr):
        self.instructions.append(f"LOAD {left_addr}")
        self.instructions.append(f"LOAD {right_addr}")
        self.instructions.append(f"CMP")

    def visit_ConditionalNode(self, node: ConditionalNode):
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()

        jump_instruction = self.visit(node.condition)  # Получаем строку из CompareNode
        if jump_instruction:  # Если была возвращена инструкция для перехода
            self.instructions.append(f"{jump_instruction} {false_label}")
        else:
            self.instructions.append(f"JUMP_IF_FALSE {false_label}")

        for stmt in node.true_branch:
            self.visit(stmt)
        self.instructions.append(f"JUMP {end_label}")

        self.instructions.append(f"{false_label}:")
        for stmt in node.false_branch:
            self.visit(stmt)
        self.instructions.append(f"{end_label}:")


    def visit_LoopNode(self, node: LoopNode):
        start_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(f"{start_label}:")
        self.visit(node.start)
        self.visit(node.end)
        self.instructions.append("SUB")
        self.instructions.append("POP")
        self.instructions.append(f"JUMP_IF_EQUAL {end_label}")

        for stmt in node.body:
            self.visit(stmt)

        self.instructions.append(f"LOAD {self.variable_table[node.start.value]}")
        self.instructions.append("INC")
        self.instructions.append(f"STORE {self.variable_table[node.start.value]}")

        self.instructions.append(f"JUMP {start_label}")
        self.instructions.append(f"{end_label}:")

    def visit_OutputNode(self, node: OutputNode):
        if isinstance(node.optional, StringNode):
            self.print_string(node.optional.value)
        elif isinstance(node.optional, FunctionCallNode):
            self.print_variable(node.optional.name)
        else:
            self.instructions.append("OUT")

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        if node.name in self.function_names:
            self.instructions.append(f"CALL {node.name}")
        elif self.variable_table.keys(node.name):
            self.instructions.append(f"PUSH {node.name}")

    def print_string(self, value: str):
        for char in value:
            ascii_code = ord(char)
            self.instructions.append(f"PUSH {ascii_code}")
            self.instructions.append("OUT")
    
    def print_variable(self, name: str):
        start_label_1 = self.new_label()
        end_label = self.new_label()

        self.instructions.append(f"{start_label_1}:")
        self.instructions.append(f"LOAD {self.variable_table["iter"] }")
        self.instructions.append(f"LOAD_TOP")
        self.instructions.append("DUP")
        self.instructions.append("PUSH 0")
        self.instructions.append("CMP")
        self.instructions.append(f"JUMP_IF_EQUAL {end_label}")

        self.instructions.append(f"LOAD {self.variable_table["iter"] }")
        self.instructions.append(f"INC")
        self.instructions.append(f"STORE {self.variable_table["iter"] }")

        self.instructions.append(f"OUT")

        self.instructions.append(f"JUMP {start_label_1}")

        self.instructions.append(f"{end_label}:")

        self.instructions.append(f"PUSH {self.data_section[self.variable_table["iter"]] }")
        self.instructions.append(f"INC")
        self.instructions.append(f"STORE {self.variable_table["iter"]}")

        self.instructions.append(f"RET")
        self.instructions.append(f"CALL {start_label_1}")



    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"
    
