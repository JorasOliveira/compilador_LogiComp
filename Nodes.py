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
            child.evaluate(symbol_table)
            
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("evaluate do print: ", self.children[0].value)
        
        if isinstance(self.children[0], int):
            result = self.children[0]
            if result != None:
                print(result)

        else:
            result = self.children[0].evaluate(symbol_table)
            if result != None:
                print(result)

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)

class Else(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table): 
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        else:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):

        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table):
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
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

        child_0 = self.children[0].evaluate(symbol_table)
        child_1 = self.children[1].evaluate(symbol_table)

        if child_0 != None and child_1 != None:
            if self.value == "+":
                return child_0 + child_1
            if self.value == "-":
                return child_0 - child_1
            if self.value == "*":
                return child_0 * child_1
            if self.value == "/":
                return child_0 // child_1
            if self.value == '||':
                return child_0 or child_1
            if self.value == "&&":
                return child_0 and child_1
            if self.value == "==":
                return (child_0 == child_1)
            if self.value == ">":
                return child_0 > child_1
            if self.value == "<":
                return child_0 < child_1

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "+":
            return self.children[0].evaluate(symbol_table)

        if self.value == "-":
            return -self.children[0].evaluate(symbol_table)
        
        if self.value == "!":
            return not self.children[0]

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, symbol_table):
        return None
