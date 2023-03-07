import re
import time
class LZ77:
    def __init__(self, buffer_length = 10, lookahead = 150):
        self.buffer_length = buffer_length
        self.lookahead = lookahead

    def compress(self, text):
        buffer = ''
        code = []
        while text:
            text, offset, length, next, buffer = self.best_matches_compress(text, buffer)
            code.append((offset, length, next))
        return code
    
    def decompress(self, code):
        buffer = ''
        massage = ''
        for i in code:
            index = len(buffer) - i[0]
            if not i[0]:
                massage += i[2]
                buffer = (buffer + i[2])[-self.buffer_length:]
            else:
                if len(buffer[index:]) > i[1]:
                    massage += buffer[index:i[1]+index] + i[2]
                    buffer = (buffer + buffer[index:i[1]+index] + i[2])[-self.buffer_length:]
                else:
                    repetition = buffer[index:]
                    repetition = (int(i[1] / len(repetition)) + 1)*repetition
                    massage += repetition[:i[1]] + i[2]
                    buffer = (buffer + repetition[:i[1]] + i[2])[-self.buffer_length:]
        return massage

    def best_matches_compress (self, data, buffer):
        offset = 0
        length = 0
        next = data[0]
        repetition = ''
        index = 0
        try:
            for i in range(1, self.lookahead):
                if index + i > len(buffer):
                    if repetition:
                        repetition = repetition * (int(self.lookahead / len(repetition)) + 1)
                        if repetition[:i] == data[:i]:
                            length = i
                            next = data[i]
                        else:
                            break 
                    else:
                        break     
                else:
                    if data[:i] in buffer:
                        index = buffer.index(data[:i])
                        repetition = buffer[index : index + i]
                        offset = len(buffer) - index
                        length = i
                        next = data[i]
                    else:
                        break
            return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])
        except IndexError:
            next = ''
            return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])

if __name__ == '__main__':
    lz = LZ77(20, 250)
    with open("test_documents/sample-75kb-text-file.txt") as file:
        data = file.read()
    start_comp = time.time()
    compressed = lz.compress(data)
    end_comp = time.time()
    start_decomp = time.time()
    decompressed = lz.decompress(compressed)
    end_decomp = time.time()
    print(data == decompressed)
    print(end_comp-start_comp, end_decomp-start_decomp)