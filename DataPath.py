
import ALU
class DataPath:
    def __init__(self, size, input_tokens):
        self.data_memory = [0] * size # Память данных
        self.input_buffer = input_tokens  # Входные данные
        self.output_buffer = []  # Буфер вывода
        self.acc = 0  # Аккумулятор
        self.stack = []  # Стек для хранения значений
        self.alu = ALU.ALU()

    def set_acc(self, value):
        self.acc = value

    def signal_push(self, value):
        self.stack.append(value)

    def signal_pop(self):
        self.stack.pop()

    def signal_store(self, addr):
        self.acc = self.stack[-1]
        self.data_memory[int(addr)] = self.acc

    def signal_store_top(self):
        self.acc = self.stack[-1]
        self.stack.pop()
        self.data_memory[int(self.acc)] = self.stack[-1]
        
    def signal_load(self, addr):
        self.acc = self.data_memory[int(addr)]
        self.stack.append(self.acc)

    def signal_load_top(self):
        self.acc = self.stack[-1]
        self.stack.pop()
        self.stack.append(self.data_memory[int(self.acc)])

    def signal_dup(self):
        self.acc = self.stack[-1]
        self.stack.append(self.acc)

    def signal_in(self):
        self.acc = self.input_buffer[0]
        self.input_buffer = self.input_buffer[1:]
        # print(self.input_buffer[1:])
        # SystemExit(0)
        self.stack.append(self.acc)

    def signal_out(self):
        self.acc = self.stack[-1]
        self.output_buffer.append(self.acc)
        

