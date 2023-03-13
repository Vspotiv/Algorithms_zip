import time
class LZ77:
    def __init__(self, buffer_length = 10):
        self.buffer_length = buffer_length

    def compress(self, text):
        read = 0
        length_data = len(text)
        buffer = ''
        code = []
        while read < length_data:
            offset, length, next, buffer, read = self.best_matches_compress(text, buffer, read)
            code.append((offset, length, next))
        return code
    
    def decompress(self, code):
        buffer = ''
        message = ''
        for i in code:
            index = len(buffer) - i[0]
            to_end = index + i[1]
            length = len(buffer[index:])
            if not i[0]:
                message += i[2]
                buffer = message[-self.buffer_length:]
            else:
                if length > i[1]:
                    message += buffer[index:to_end] + i[2]
                    buffer = message[-self.buffer_length:]
                else:
                    repetition = (int(i[1] / length) + 1) * buffer[index:]
                    message += repetition[:i[1]] + i[2]
                    buffer = message[-self.buffer_length:]
        return message

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
        except IndexError:
            next = ''
        return (offset, length, next, (buffer + message)[-self.buffer_length:], position + 1)


if __name__ == '__main__':
    lz = LZ77(100)
    with open("test_documents/sample-2mb-text-file.txt") as file:
        data = file.read()
    start_comp = time.time()
    compressed = lz.compress(data)
    end_comp = time.time()
    start_decomp = time.time()
    decompressed = lz.decompress(compressed)
    end_decomp = time.time()
    print(decompressed == data)
    print(end_comp-start_comp, end_decomp - start_decomp, len(compressed))