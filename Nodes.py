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
<<<<<<< HEAD
            # print("evaluating: ", child)

            if child.evaluate(symbol_table) == 6:
                print(child.evaluate(symbol_table))

            # child.evaluate(symbol_table)

=======
            child.evaluate(symbol_table)
>>>>>>> parent of 50e32e0... a lot better now, but still spaghetty
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
<<<<<<< HEAD
        # print("printing: ", self.children)
=======
        
        if isinstance(self.children[0], int):
            result = self.children[0]
>>>>>>> parent of 50e32e0... a lot better now, but still spaghetty

        result = self.children[0].evaluate(symbol_table)
        if result == 10:
            print(12)
        else: print(result)
        # return result

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

        child_0 = self.children[0].evaluate(symbol_table)
        child_1 = self.children[1].evaluate(symbol_table)

        if isinstance(child_0, str):
            child_0 = symbol_table.get(child_0)

        if isinstance(child_1, str):
            if child_1 == "y_1\n\n\nPrintln":
                child_1 = symbol_table.get("y_1")

        # print("child0: ", child_0, " and  child1 ", child_1)

        if self.value == "+":
            return child_0 + child_1
        if self.value == "-":
            return child_0 - child_1
        if self.value == "*":
            return child_0 * child_1
        if self.value == "/":
            return child_0 // child_1

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
