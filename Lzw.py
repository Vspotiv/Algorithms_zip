class Lzw:
    def __init__(self, sequence):
        self.sequence = sequence
        self.dict_encodes = dict()
        self.dict_decodes = dict()
        self.codes = list()

    def encode(self):
        code_number = 0

        for symbol in sorted(list(set(self.sequence))):
            self.dict_encodes[symbol] = code_number
            self.dict_decodes[code_number] = symbol
            code_number += 1

        while len(self.sequence) != 1:
            symbols = self.sequence[:2]
            cropper = 2

            if symbols not in self.dict_encodes.keys():
                self.codes.append(self.dict_encodes[symbols[0]])
                self.dict_encodes[symbols] = code_number
                self.dict_decodes[code_number] = symbols
                self.sequence = self.sequence[1:]

                code_number += 1


            else:
                while symbols in self.dict_encodes.keys():
                    symbols = ''.join([symbols, self.sequence[cropper]])
                    cropper += 1

                self.dict_encodes[symbols] = code_number
                self.dict_decodes[code_number] = symbols
                self.codes.append(self.dict_encodes[symbols[:-1]])
                self.sequence = self.sequence[cropper-1:]

                code_number += 1

        self.codes.append(self.dict_encodes[self.sequence[0]])
        return self.codes

    def decode(self):
        decoded_string = ''
        for code in self.codes:
            decoded_string = decoded_string + self.dict_decodes[code]
        return decoded_string
