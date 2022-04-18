# -in   input file
# -out  output file
# -m    mode
# -c    code word for algorithm
# -s    should show the encr text
# -t    if just text

import sys
from random import randrange

def CycleShift(let, shift):
    if not let.isalpha():
        return let
    first = 'a' if let.islower() else 'A'
    return chr(ord(first) + (ord(let) - ord(first) + shift) % 26)


def CaesarCipher(task_info):
    text = task_info.InputText()
    encrypted_text = ""
    for let in text:
        encrypted_text += CycleShift(let, task_info.code)
    task_info.OutputWrite(encrypted_text)
    if task_info.show:
        print(encrypted_text)


def VegenereCipher():
    pass


class TaskData:
    __fields_names = {"-in" : "input_name", "-out" : "output_name",\
                      "-m": "mode", "-c" : "code", "-s" : "show", "-t" : "text"}

    def __init__(self, args):
        self.show = False
        i = 0
        while i < len(args):
            if args[i] in self.__fields_names and args[i] != "-s":
                setattr(self, self.__fields_names[args[i]], args[i + 1])
                i += 2
            elif args[i] == "-s":
                self.show = True
                i += 1
        if not hasattr(self, "output_name") and hasattr(self, "input_name"):
            self.output_name = f"encrypted_{self.input_name}"
        elif not hasattr(self, "output_name"):
            self.output_name = "enctypted_file.txt"
        if not hasattr(self, "code"):
            self.SetDefaultCode()

    def SetDefaultCode(self):
        if self.mode == "caesar":
            self.code = randrange(1, 25)
        elif self.mode == "vegenere":
            self.code = "icensq"
        elif self.mode == "vernum":
            pass

    def OutputWrite(self, text):
        with open(self.output_name, 'w') as fout:
            fout.write(text)

    def InputText(self):
        result = ""
        if hasattr(self, "input_name"):
            with open(self.input_name, 'r') as fin:
                result = fin.read()
            return result
        return self.text

    # def CorrectData(self):
    #     if not hasattr


def Caller(task_info):
    if task_info.mode == "caesar":
        CaesarCipher(task_info)
    elif task_info.mode == "vegenere":
        VegenereCipher(task_info)
    elif task_info.mode == "vernum":
        VernumCipher(task_info)
    else:
        pass # havent't developed yet

if __name__ == "__main__":
    Caller(TaskData(sys.argv[1:]))