class Node:
    def __init__(self, value=None, symbol=None, is_leaf=False, lc=None, rc = None):
        self.value = value
        self.symbol = symbol
        self.left_children = lc
        self.right_children = rc
        self.is_leaf = is_leaf
        self.code = None

class Huffman_code:
    def __init__(self, sequence):
        self.sequence = sequence
        self.stats = []
        self.root = None
        self.codes = dict()

    def calculate_probabities(self):
        for symbola in set(self.sequence):
            self.stats.append(Node(value = self.sequence.count(symbola), symbol=symbola, is_leaf=True))
        self.stats = sorted(self.stats, key=lambda x: x.value, reverse=True)

    def create_tree(self):
        while len(self.stats) != 1:
            self.creation(self.stats[-1], self.stats[-2])

    def creation(self, node_right, node_left):
        if len(self.stats) != 2:
            self.stats = self.stats[:-2]
            self.stats.append(Node(value = node_left.value + node_right.value, rc = node_right, lc = node_left))
            self.stats = sorted(self.stats, key=lambda x: x.value, reverse=True)
        else:
            self.root = Node(value = node_left.value + node_right.value, rc = node_right, lc = node_left)
            self.stats = [Node(value = node_left.value + node_right.value, rc = node_right, lc = node_left)]

    def get_codes(self, root, code=''):
        try:
            if root.is_leaf:
                root.code = code
                self.codes[root.symbol] = root.code
            self.get_codes(root.left_children, code=code + '0')
            self.get_codes(root.right_children, code=code + '1')

        except AttributeError:
            None

    def calculate_encode(self):
        result = ''
        self.calculate_probabities()
        self.create_tree()
        self.get_codes(self.root)
        for element in self.sequence:
            result = result + self.codes[element]
        return result

    def huffman_decode(self, code):
        current_node = self.root
        decoded_string = ""

        for bit in code:
            if bit == "0":
                current_node = current_node.left_children
            else:
                current_node = current_node.right_children

            if current_node.is_leaf:
                decoded_string += current_node.symbol
                current_node = self.root

        return decoded_string
