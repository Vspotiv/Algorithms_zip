import re

class LZ77:
    def __init__(self, buffer_length = 10):
        self.buffer_length = buffer_length
        self.lookahead = 150

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
            if len(massage) > 900:
                print(2)
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
                            return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])
                    else:
                        return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])
                else:
                    if data[:i] in buffer:
                        index = [m.start() for m in re.finditer(data[:i], buffer)][-1]
                        repetition = buffer[index : index + i]
                        offset = len(buffer) - index
                        length = i
                        next = data[i]
                    else:
                        return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])
            return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length+1:])
        except IndexError:
            next = ''
            return (data[i:], offset, length, next, (buffer + data[:i])[-self.buffer_length:])

if __name__ == '__main__':
    lz = LZ77(15)
    with open("sample3.txt") as file:
        data = file.read()
    compressed = lz.compress(data)
    decompressed = lz.decompress(compressed)
    print(data == decompressed)