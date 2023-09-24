from SymbolTable import SymbolTable

class Node:
    def __init__(self, value, children):
        self.value = value  # value of the node, can be int or str
        self.children = children  # list of Node

    def evaluate(self, symbol_table):
        return self.value
        
class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            # print("evaluating: ", child.value)
            child.evaluate(symbol_table)

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        # print("atemting to get: ", self.value)
        return symbol_table.get(self.value)

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print(self.children)
        
        if isinstance(self.children[0], int):
            result = self.children[0]

        else: result = self.children[0].evaluate(symbol_table)

        print(result)
        return result

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("adding key: ", self.children[0], " value: ", self.children[1])
        if self.children[1] is not None:
            value = self.children[1].evaluate(symbol_table)
            symbol_table.set(self.children[0], value)

        else: 
            symbol_table.set(self.children[0], self.children[1])
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return self.value

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "+":
            return self.children[0].evaluate(symbol_table) + self.children[1].evaluate(symbol_table)
        if self.value == "-":
            return self.children[0].evaluate(symbol_table) - self.children[1].evaluate(symbol_table)
        if self.value == "*":
            return self.children[0].evaluate(symbol_table) * self.children[1].evaluate(symbol_table)
        if self.value == "/":
            return self.children[0].evaluate(symbol_table) // self.children[1].evaluate(symbol_table)

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "+":
            return self.children[0].evaluate(symbol_table)

        if self.value == "-":
            return -self.children[0].evaluate(symbol_table)

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, symbol_table):
        return None
