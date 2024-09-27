import json

class AssmToJson:
    def __init__(self, asm_code: str):
        self.asm_code = asm_code
        self.json_instructions = []
        self.labels = {}
        self.labels_code = []
        self.main_code = []

    def convert(self):
        lines = self.asm_code.strip().splitlines()
        i = -1
        label = 0
        inner_label = []
        copy = []
        inner_lables_code = {}
        instruction = {
                        "opcode": "MAIN"
                    }
        self.main_code.append(instruction)

        for line in lines:
            i += 1
            # Удалим возможные пробелы или табуляцию в начале строки
            line = line.strip()

            # Разделим строку на опкод и операнд(ы)
            parts = line.split()
            if len(parts) > 0:
                if len(copy) > 0:
                    # print('in', inner_label)
                    copy.pop()
                    continue
                
                if parts[0][-1] == ":":  # Если это метка
                    
                    # print("lable", parts[0].lower())

                    if label == 0 or parts[0][:-1].upper() == parts[0][:-1]: # Если мы не в блоке метки
                        label_name = parts[0][:-1]
                        if label_name not in self.labels:
                            self.labels[label_name] = len(self.labels_code)
                        label = 1
                        continue
                    else:  
                        label_name = parts[0][:-1]
                        
                        l = i                     
                        for j in range(2):
                            l = l + 1
                            next_line = lines[l].strip()
                            next_parts = next_line.split()
                            if len(next_parts) > 0:
                                instruction = {"opcode": next_parts[0]}
                                if len(next_parts) > 1:
                                    instruction["operand"] = " ".join(next_parts[1:])
                                inner_label.append(instruction)
                                copy.append(instruction)
                        
                        if label_name not in inner_lables_code:
                            # print("popopo", copy)
                            inner_lables_code[label_name] = copy[:]

                        
                        continue

                if label == 1:  # Обрабатываем основную метку
                    instruction = {
                        "opcode": parts[0]
                    }

                    if len(parts) > 1:
                        if parts[1] in self.labels:
                            instruction["operand"] = " " + str(self.labels[parts[1]])
                        else:
                            instruction["operand"] = " ".join(parts[1:])

                    self.labels_code.append(instruction)
                    if parts[0] == "RET":  # Возвращаемся в основной код, если встретили RET
                        label = 0
                        for key in inner_lables_code:
                            if key not in self.labels:
                                self.labels[key] = len(self.labels_code)
                                # print("inner_lables_code", inner_lables_code)
                                for k in inner_lables_code[key]:
                                    # print("k", k)
                                    self.labels_code.append(k)
                        # print("self.labels_code", self.labels_code)        
                        inner_label.clear
                        inner_lables_code.clear
                elif label == 0:  # Обработка основного кода
                    instruction = {
                        "opcode": parts[0]
                    }

                    if len(parts) > 1:
                        if parts[1] in self.labels:
                            instruction["operand"] = " " + str(self.labels[parts[1]])
                        else:
                            instruction["operand"] = " ".join(parts[1:])

                    self.main_code.append(instruction)

        # Объединяем код меток и основной код
        self.json_instructions = self.labels_code + self.main_code

        # Обновляем операнды меток
        for instruction in self.json_instructions:
            if len(instruction) > 1 and instruction["operand"] in self.labels:
                instruction["operand"] = " " + str(self.labels[instruction["operand"]])

        for i in range(len(self.json_instructions)):
            print(i, self.json_instructions[i])
        print(self.labels)

        return self.json_instructions

    def save_to_file(self, output_filename: str):
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(self.json_instructions, outfile, ensure_ascii=False, indent=4)

    # @staticmethod
    # def read_and_print_json(filename: str):
    #     try:
    #         # Открываем файл для чтения
    #         with open(filename, 'r', encoding='utf-8') as infile:
    #             # Загружаем содержимое файла как JSON
    #             json_data = json.load(infile)
    #             # Выводим содержимое JSON
    #             print(json.dumps(json_data, ensure_ascii=False, indent=4))
    #     except FileNotFoundError:
    #         print(f"Файл {filename} не найден.")
    #     except json.JSONDecodeError:
    #         print(f"Ошибка декодирования JSON в файле {filename}.")
