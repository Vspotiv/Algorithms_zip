import re
import time
class LZ77:
    def __init__(self, buffer_length = 10, lookahead = 150):
        self.buffer_length = buffer_length
        self.lookahead = lookahead

    def compress(self, text):
        read = 0
        length_data = len(text)
        buffer = ''
        code = []
        while read < length_data:
            offset, length, next, buffer, read = self.best_matches_compress(text, buffer, read)
            read += 1
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

    def best_matches_compress (self, data, buffer, position):
        offset = 0
        length = 0
        buf_len = len(buffer)
        index = 0
        message = ''
        next = data[position]
        try:
            while True:
                message += next
                if index + length > buf_len:
                    if repetition:
                        if repetition[length % len_rep] == data[position]:
                            length += 1
                            position += 1
                            next = data[position]
                        else:
                            break 
                    else:
                        break     
                else:
                    if message in buffer:
                        index = buffer.index(message)
                        offset = buf_len - index
                        length += 1
                        position += 1
                        next = data[position]
                        repetition = buffer[index:]
                        len_rep = len(repetition)
                    else:
                        break
            return (offset, length, next, (buffer + message)[-self.buffer_length:], position)
        except IndexError:
            next = ''
            return (offset, length, next, (buffer + message)[-self.buffer_length:], position)


if __name__ == '__main__':
    lz = LZ77(100)
    with open("test_documents/sample-2mb-text-file.txt") as file:
        data = file.read()
    # data = 'hellothere'
    start_comp = time.time()
    compressed = lz.compress(data)
    # print(compressed)
    end_comp = time.time()
    # start_decomp = time.time()
    decompressed = lz.decompress(compressed)
    # print(decompressed)
    # end_decomp = time.time()
    # print(data == decompressed)
    print(decompressed == data)
    print(end_comp-start_comp, len(compressed))