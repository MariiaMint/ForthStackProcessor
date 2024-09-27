class ALU:
    def __init__(self):
        self.flags = {"N": 0, "Z": 0}
        

    def run_alu2(self, signal: str, a: float, b: float):
        if (signal == "ADD"):
            return self.signal_add(a, b)
        if (signal == "SUB"):
            return self.signal_sub(a, b)
        if (signal == "MUL"):
            return self.signal_mul(a, b)
        if (signal == "DIV"):
            return self.signal_div(a, b)
        if (signal == "AND"):
            return self.signal_and(a, b)
        if (signal == "OR"):
            return self.signal_or(a, b)
        if (signal == "CMP"):
            self.signal_cmp(a, b)

    def run_alu1(self, signal: str, a: float):
        if (signal == "INC"):
            return self.signal_inc(a)
        if (signal == "DEC"):
            return self.signal_dec(a)
        
    def set_flags(self, result):
        if result == 0:
            self.flags["Z"] = 1 
        if result != 0:
            self.flags["Z"] = 0 
        if result < 0:
            self.flags["N"] = 1 
        if result >= 0:
            self.flags["N"] = 0 
        
    def signal_add(self, a, b):
        res = float(a) + float(b)
        self.set_flags(res)
        return res

    def signal_sub(self, a, b):
        res = float(a) - float(b)
        self.set_flags(res)
        # print("res",a, b, res, int(res), self.flags)
        return res

    def signal_mul(self, a, b):
        res = float(a) * float(b)
        self.set_flags(res)
        return res

    def signal_div(self, a, b):
        if b != 0:
            res = float(a) / float(b)
            self.set_flags(res)
            # print("res", res, int(res), self.flags)
            return int(res)
        else:
            raise ZeroDivisionError("Division by zero")
        
    def signal_and(self, a, b):
        res = -int(bool(a) and bool(b))
        self.set_flags(res)
        return res
    
    def signal_or(self, a, b):
        res = -int(bool(a) or bool(b))
        self.set_flags(res)
        return res

    def signal_cmp(self, a, b):
        # print("a, b:", a, b)
        
        try:
            # Попытка преобразовать a и b к float
            a_float = float(a)
            b_float = float(b)
            res = a_float - b_float  # Если преобразование успешно, вычитаем
        except ValueError:
            # Если преобразование не удалось, сравниваем строки
            if str(a) == str(b):
                res = 0
            else:
                res = 1
        
        self.set_flags(res)


    def signal_inc(self, a):
        res = int(a) + 1
        self.set_flags(res)
        return res
    
    def signal_dec(self, a):
        res = int(a) - 1
        self.set_flags(res)
        return res
