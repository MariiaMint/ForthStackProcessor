import json
import time
class ControlUnit:
    def __init__(self, program, data_path):
        self.program = program
        self.data_path = data_path
        self.program_counter = 0
        self.instruction_register = None
        self.status_register = "00"
        self.buffer_register = 0
        self.call_stack = []  

    def decode_instructions(self):
        with open(self.program, 'r', encoding='utf-8') as file:
            self.program = json.load(file)

    def latch_pc(self, value=None):
        if value is not None:
            self.program_counter = value
        else:
            self.program_counter += 1

    def latch_ir(self, opcode):
        self.instruction_register = opcode

    def latch_br(self, operand):
        self.buffer_register = operand
    
    def latch_sr(self):
        self.status_register = str(self.data_path.alu.flags["N"]) + str(self.data_path.alu.flags["Z"])

    def run(self):
        for i in range(len(self.program)):
            instr = self.program[i]
            # print(instr)
            if instr["opcode"] == "MAIN":
                self.latch_pc(i+1)
                # print("main", self.program_counter)
                break
        while self.program_counter < len(self.program):
            instr = self.program[self.program_counter]
            self.latch_ir(instr["opcode"])
            operand = instr.get("operand")
            self.latch_br(operand)

            # print(f"pc {self.program_counter}, instr {instr["opcode"]}"  )
            # print(f"stack{self.data_path.stack[:9]}, mem{self.data_path.data_memory[:8]}")
            # print("output", self.data_path.output_buffer)
            # print()
            # time.sleep(0.1)

            self.execute_instruction()
            
    def execute_instruction(self):
        instr = self.instruction_register

        if instr == "PUSH":
            self.data_path.signal_push(self.buffer_register)
            self.latch_pc()
            # print(self.program_counter)
            # SystemExit
        elif instr == "STORE":
            self.data_path.signal_store(self.buffer_register)
            self.data_path.signal_pop()
            self.latch_pc()
        elif instr == "STORE_TOP":
            self.data_path.signal_store_top()
            self.data_path.signal_pop()
            self.latch_pc()
        elif instr == "LOAD":
            self.data_path.signal_load(self.buffer_register)
            self.latch_pc()
        elif instr == "LOAD_TOP":
            self.data_path.signal_load_top()
            self.latch_pc()
        elif instr == "DUP":
            self.data_path.signal_dup()
            self.latch_pc()
        elif instr == "POP":
            self.data_path.signal_pop()
            self.latch_pc()
        elif instr == "OUT":
            self.data_path.signal_out()
            self.data_path.signal_pop()
            self.latch_pc()
        elif instr == "IN":
            self.data_path.signal_in()
            self.latch_pc()
        elif instr in ["ADD", "SUB", "MUL", "DIV", "AND", "OR", "CMP"]:

            self.data_path.set_acc(self.data_path.stack[-1])
            self.data_path.signal_pop()
            res = self.data_path.alu.run_alu2(instr, self.data_path.stack[-1],self.data_path.acc)
            
            self.latch_sr()
            
            self.data_path.signal_pop()
            if res != None:
                self.data_path.signal_push(res)
            # print("comp", self.status_register)
            # SystemExit
            self.latch_pc()
            # print(self.data_path.stack)
        elif instr in ["INC", "DEC"]:
            res = self.data_path.alu.run_alu1(instr, self.data_path.stack[-1])
            self.latch_sr()
            self.data_path.signal_pop()
            self.data_path.signal_push(res)
            self.latch_pc()
        elif instr == "JUMP":
            self.latch_pc(int(self.buffer_register))
        elif instr == "JUMP_IF_EQUAL":
            if self.status_register[1] == "1": 
                self.latch_pc(int(self.buffer_register))
                # print("self.buffer_register", self.buffer_register)
                # SystemExit
            else:
                self.latch_pc()
        elif instr == "JUMP_IF_FALSE":
            if self.status_register[1] == "0": 
                self.latch_pc(int(self.buffer_register))
            else:
                self.latch_pc()
        elif instr == "JUMP_IF_GREATER":
            # print("flags", self.status_register[0])
            if self.status_register[0] == "0":
                self.latch_pc(int(self.buffer_register))
            else:
                self.latch_pc()

        elif instr == "CALL":
            
            self.call_stack.append(self.program_counter + 1)
            self.latch_pc(int(self.buffer_register))

        elif instr == "RET":
            
            if self.call_stack:
                return_address = self.call_stack.pop()
                self.latch_pc(return_address)
            else:
                raise Exception("Call stack is empty. Cannot return.")
