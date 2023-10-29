from SymbolTable import SymbolTable

class Node:
    def __init__(self, value, children):
        self.value = value  # value of the node, can be int or str
        self.children = children  # list of Node

    def evaluate(self, symbol_table):
        return self.value
        

#TODO -> terminar de cuidar dos retornos corretos
#TODO -> implementar a tipagem forte
class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.children[1] is not None:
            # print("atempting to put:", self.children[0], self.children[1].value)
            node = self.children[1].evaluate(symbol_table)
            # print("atempting to put in symbol table: ",self.children[0], node[0], node[1])

            symbol_table.set(self.children[0], node[0], node[1])
            
        else: 
            # print("atempting to put (child[1] is none?):", self.value, self.children)
            symbol_table.set(self.children[0], self.value, self.children[1])
        
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if isinstance(self.children[0], int):
            result = self.children[0]
            if result != None:
                print(result[1])

        else:
            result = self.children[0].evaluate(symbol_table)
            if result != None:
                print(result[1])

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)

class Else(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table): 
        if self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)[1]
        else:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self, symbol_table):

        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)[1]:
            
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)

class Type(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("varDec Node: ", self.value, self.children)
        return(self.children[0], self.children[1].evaluate(symbol_table))

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return ("int", self.value)
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return ("str", self.value)
    
class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        child_0 = self.children[0].evaluate(symbol_table)
        child_1 = self.children[1].evaluate(symbol_table)

        if child_0 != None and child_1 != None:
            if self.value == "+":
                return ("int", child_0[1] + child_1[1])
            if self.value == "-":
                return ("int", child_0[1] - child_1[1])
            if self.value == "*":
                return ("int", child_0[1] * child_1[1])
            if self.value == "/":
                return ("int", child_0[1] // child_1[1])
            #because of go, we return 1 or 0 for booleans
            if self.value == '||':
                if child_0[1] or child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)
            if self.value == "&&":
                if child_0[1] and child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)
            if self.value == "==":
                if (child_0[1] == child_1[1]):
                    return ("int", 1)
                else: return ("int", 0) 
            if self.value == ">":
                if child_0[1] > child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)
            if self.value == "<":
                if child_0[1] < child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)
            if self.value == ".":
                return ("str", str(child_0[1]) + str(child_1[1]))

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "+":
            return ("int", self.children[0].evaluate(symbol_table)[1])

        if self.value == "-":
            return ("int", -self.children[0].evaluate(symbol_table)[1])
        
        if self.value == "!":
            return ("int",  not self.children[0])

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, symbol_table):
        return None
