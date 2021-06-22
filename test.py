import re
import json


sel = input("How do you want to enter the files' paths?\nEnter 1 if you want to enter them through the cmd input\nor press 2 if you want to enter them through a JSON file.\n")

while True:
    #'1' selects CMD input mode
    if sel == '1':
        cpp_file = input("Please enter C++ file path\n")
        top_function = input("Please enter the top function prototype\n")
        addresses_file = input("Please enter the addresses file path\n")
        break
    #'2' selects JSON file input mode, don't know if keeping both of the input mode is needed
    elif sel == '2':
        json_file = input("Please enter JSON file path\n")
        with open(json_file) as input_file:
            input_file = json.load(input_file)
            cpp_file = input_file["C++ file"]
            top_function = input_file['Top function']
            addresses_file = input_file['Addresses file']
        break
    else:
        print('Please insert a valid input')
        sel = input()

interface = ""

#basically a switch case
axi_type = {
    "s_axilite" : "AXI LITE",
    "axis" : "AXI Stream",
    #TODO: how do recognize axi Master?
    "m_axi" : "AXI Master"
}

data_signals = {}
#TODO: adding input/output addresses, create final classes

#this function detecs the type of interface used
try:
    with open(cpp_file) as file:
        file_as_string = file.read().split("\n")
        for string in file_as_string:
            if top_function in string:
                i = file_as_string.index(string)
                file_as_string = file_as_string[i:]
        for line in file_as_string:
            if "pragma" in line:
                line = line.split(" ")
                for word in line:
                    if "axi" in word:
                        interface = axi_type[word]
                        break
except:
    print("Please enter a valid C++ file path\n")
    cpp_file = input()

#detecting how the memory is split in addresses
try:
    with open(addresses_file) as file:
        file_as_string = file.read().split("\n")
        #reading addresses here. Not sure what to do with these
        for line in  file_as_string:
            if "//" not in line:
                break
            if "Control signals" in line:
                control_signals_offset = re.search('0x[0-9][0-9]', line)
            elif "Global Interrupt Enable Register" in line:
                global_interrupt_enable_register_offset = re.search('0x[0-9][0-9]', line)
            elif "IP Interrupt Enable Register (Read/Write)" in line:
                ip_interrupt_enable_offset = re.search('0x[0-9][0-9]', line)
            elif "IP Interrupt Status Register (Read/TOW)" in line:
                ip_interrupt_status_register_offset = re.search('0x[0-9][0-9]', line)
            elif "Data signal of" in line:
                letter = re.search('Data signal of ([a-z])', line)
                data_signals[letter[1]] = ''
except:
    print("Please enter a valid addresses file path\n")
    addresses_file = input()