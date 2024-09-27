import logging
import json

import ControlUnit
import DataPath
    
if __name__ == "__main__":
    with open("input.txt", 'r', encoding='utf-8') as file:
            input_tokens = json.load(file)
            print("input", input_tokens)
    datapath = DataPath.DataPath(100, input_tokens)
    cu = ControlUnit.ControlUnit("output.json", datapath)
    cu.decode_instructions()
    # print("decoded")
    cu.run()
    print("out", cu.data_path.output_buffer)
    print("stack", cu.data_path.stack)
    print("mem", cu.data_path.data_memory)