# -i    input file
# -o    output file
# -m    mode, which algorithm or hack
# -k    key for the algorithm
# -s    should show the encrypted text
# -t    if just text
# -d    decoding

# work is guaranteed only for utf-8 english letters


import sys
from random import randrange, sample
from collections import Counter
from copy import copy


kEngLetters = [chr(let_ord) for let_ord in range(ord('a'), ord('a') + 26)]
kEngLettersFrequency = {'a' : 8.5,
                        'b' : 2,
                        'c' : 4.5,
                        'd' : 3.4,
                        'e' : 11.2,
                        'f' : 1.8,
                        'g' : 2.5,
                        'h' : 3,
                        'i' : 7.5,
                        'j' : 0.2,
                        'k' : 1.1,
                        'l' : 5.5,
                        'm' : 3,
                        'n' : 6.7,
                        'o' : 7.2,
                        'p' : 3.1,
                        'q' : 0.2,
                        'r' : 7.6,
                        's' : 5.7,
                        't' : 7,
                        'u' : 3.6,
                        'v' : 1,
                        'w' : 1.3,
                        'x' : 0.3,
                        'y' : 1.8,
                        'z' : 0.3}
for let in kEngLetters:
    kEngLettersFrequency[let] /= 100


def alphabet_ord(let):
    first = 'a' if let.islower() else 'A'
    return ord(let) - ord(first)


def letter_cycle_shift(let, shift):
    if not let.isalpha():
        return let
    first = 'a' if let.islower() else 'A'
    return chr(ord(first) + (alphabet_ord(let) + shift) % 26)


def text_cycle_shift(text, shift):
    result = ""
    for let in text:
        result += letter_cycle_shift(let, shift)
    return result


def get_frequency(x, counter): 
   return counter[x] / total(counter)


def total(counter): #there is a method with the same name, but i have only py3.8
    result = 0
    for pair in counter.items():
        if pair[0].isalpha():
            result += pair[1]
    return result


def stretcher(word, length):
    start_len = len(word)
    word *= length // start_len
    while len(word) != length:
        word += word[-start_len]
    return word


def caesar_cipher(task):
    encrypted_text = text_cycle_shift(task.InputText(), task.key)
    task.ShowResult(encrypted_text)


def decode_caesar_cipher(task):
    text = text_cycle_shift(task.InputText(), -task.key)
    task.ShowResult(text)


def hack_caesar_cipher(task):
    encrypted_text = task.InputText()
    encrypted_text.lower()
    lets_frequency = Counter(encrypted_text)
    min_total_error_rate = 100
    for shift in range(26):
        total_error_rate = 0
        for let in kEngLetters:
            after_shift = letter_cycle_shift(let, shift)
            total_error_rate += abs(get_frequency(after_shift, lets_frequency)\
                                        - kEngLettersFrequency[let]) ** 2
        if total_error_rate < min_total_error_rate:
            min_total_error_rate, task.key = total_error_rate, shift
    decode_caesar_cipher(task)


def vegenere_cipher(task):
    text = task.InputText()
    encrypted_text = ""
    key_text = stretcher(task.key, len(text))
    for let, key_let in zip(text, key_text):
        if not let.isalpha():
            encrypted_text += let
        else:
            first = 'a' if let.islower() else 'A' 
            encrypted_text += letter_cycle_shift(first,\
                                      alphabet_ord(let) + alphabet_ord(key_let))
    task.ShowResult(encrypted_text)


def decode_vegenere_cipher(task):
    text = ""
    encrypted_text = task.InputText()
    key_text = stretcher(task.key, len(encrypted_text))
    for encrypted_let, key_let in zip(encrypted_text, key_text):
        if not encrypted_let.isalpha():
            text += encrypted_let
        else:
            first = 'a' if encrypted_let.islower() else 'A' 
            text += letter_cycle_shift(first,\
                            alphabet_ord(encrypted_let) - alphabet_ord(key_let))
    task.ShowResult(text)


def vernum_cipher(task):
    byte_text = ByteString(task.InputText())
    byte_key = ByteString(task.key)
    encrypted_byte_array = byte_text ^ byte_key
    encrypted_byte_array.Rise(ord(' '))
    task.ShowResult(encrypted_byte_array.ToString())


def decode_vernum_cipher(task):
    encrypted_byte_array = ByteString(task.InputText())
    encrypted_byte_array.Rise(ord(' ') * -1)
    byte_key = ByteString(task.key)
    text = (encrypted_byte_array ^ byte_key).ToString()
    task.ShowResult(text)


class ByteString:
    def __init__(self, string=None):
        if string:
            self.len = len(string)
            self.bytes = [ord(let) for let in string]
        else:
            self.len = 0
            self.bytes = []

    def __ixor__(self, other):
        for i in range(self.len):
            self.bytes[i] ^= other.bytes[i]
        return self

    def __xor__(self, other):
        result = self.Copy()
        result ^= other
        return result

    def ToString(self):
        result = str()
        for let_ord in self.bytes:
            result += chr(let_ord)
        return result

    def Copy(self):
        result = ByteString()
        result.bytes = self.bytes[:]
        result.len = self.len
        return result

    def Rise(self, up):
        for i in range(len(self.bytes)):
            self.bytes[i] += up


class Task:
    __fields_names = {"-i" : "input_name", "-o" : "output_name",
                      "-m": "mode", "-k" : "key", "-s" : "show",
                      "-t" : "text", "-d" : "decode"}

    def __init__(self, args):
        self.show = False
        self.decode = False
        i = 0
        while i < len(args):
            if args[i] == "-s":
                self.show = True
                i += 1
            elif args[i] == "-d":
                self.decode = True
                i += 1
            elif args[i] in self.__fields_names and args[i] != "-s":
                setattr(self, self.__fields_names[args[i]], args[i + 1])
                i += 2
        if self.mode == "hack":
            self.decode = True
        self.SetOutputFile()
        self.SetKey()

    def SetOutputFile(self):
        if hasattr(self, "output_name"):
            return
        prefix = "decoded" if self.decode else "encrypted"
        if not hasattr(self, "output_name") and hasattr(self, "input_name"):
            self.output_name = f"{prefix}_{self.input_name}"
        elif not hasattr(self, "output_name"):
            self.output_name = f"{prefix}_file.txt"

    def SetKey(self):
        if hasattr(self, "key") and self.mode == "caesar":
            self.key = int(self.key)
        if hasattr(self, "key") or self.mode == "hack":
            return
        if not hasattr(self, "key"):
            if self.mode == "caesar":
                self.key = randrange(1, 25)
            elif self.mode in ("vegenere", "vernum"):
                self.key = ''.join(sample(kEngLetters, len(self.InputText())))
        print(f"Your key is {self.key}\n")

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

    def ShowResult(self, result):
        self.OutputWrite(result)
        if self.show:
            print(result)


def Caller(task):
    if task.mode == "hack":
        hack_caesar_cipher(task)
    elif task.mode == "caesar" and task.decode:
        decode_caesar_cipher(task)
    elif task.mode == "caesar":
        caesar_cipher(task)
    elif task.mode == "vegenere" and task.decode:
        decode_vegenere_cipher(task)
    elif task.mode == "vegenere":
        vegenere_cipher(task)
    elif task.mode == "vernum" and task.decode:
        decode_vernum_cipher(task)
    elif task.mode == "vernum":
        vernum_cipher(task)


if __name__ == "__main__":
    Caller(Task(sys.argv[1:]))
