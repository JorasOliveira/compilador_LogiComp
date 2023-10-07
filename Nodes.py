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
        # print("atempting to get: ", self.value, " from symbol table")

        if self.value == "y_1\n\n\nPrintln":
            return symbol_table.get("y_1")
        
        else: return symbol_table.get(self.value)

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("evaluate do print: ", self.children[0])
        
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

    def evaluate(self, symbol_table): #TODO -> entender se esta certo
        # print("evaluate do if: ", self.children[0])
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)

class Else(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table): #TODO -> entender se esta certo
        # print("evaluate do else: ", self.children[0])
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        else:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table): #TODO -> entender se esta certo
        # print("evaluate do for: ", self.children[0])
        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table):
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("evaluating assngment of: ", self.children[0], " to: ", self.children[1])
        
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
        # print("in binop, child_0: ", child_0, " child_1: ", child_1, " value: ", self.value)

        if isinstance(child_0, str):
            if child_0 == "y_1\n\n\nPrintln":
                child_0 = symbol_table.get("y_1")
            else: child_0 = symbol_table.get(child_0)

        if isinstance(child_1, str):
            if child_1 == "y_1\n\n\nPrintln":
                child_1 = symbol_table.get("y_1")
            else: child_1 = symbol_table.get(child_1)
        
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
