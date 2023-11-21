from SymbolTable import SymbolTable
import Nodes

funcTable = SymbolTable()

# main_call = 0

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
        # print("self.children: ", self.children)
        # print("children of type: ", self.children[-1].value)
        if_funcDec = self.children[-1].value

        for child in self.children:
            if child.value == "Return":
                result = child.evaluate(symbol_table)
                return result
            else: child.evaluate(symbol_table)

        if if_funcDec == "FuncDec":
            main = self.children[-1].children[0].children[0].value

            if main != "main":
                raise Exception("ERROR: No main function")
            else: Nodes.FuncCall("main", ["main",[]]).evaluate(symbol_table)

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("assingment: ", self.children)
        if self.children[1] is not None:
            # print("assingment.children: ", self.children[1])
            node = self.children[1].evaluate(symbol_table)
            # print("just evaluated: ", self.children[1])
            # print("node: ", node) 

            if node is not None:
                # print("atempting to put in symbol table: ",self.children[0], node[0], node[1]) 
                # print(symbol_table.get(self.children[0]))

                if (isinstance(symbol_table.get(self.children[0])[0], Type)):
                    if (symbol_table.get(self.children[0])[0].value != node[0]):
                        raise Exception("Wrong Type")
                    
                elif symbol_table.isIn(self.children[0]):
                    if (symbol_table.get(self.children[0])[0] != node[0]):
                        raise Exception("Wrong Type")

                if node[0] == "int":
                    if isinstance(node[1], str):
                        raise Exception("Syntax Error")

                if node[0] == "string":
                    if isinstance(node[1], int) or isinstance(node[1], float):
                        raise Exception("Syntax Error")

                symbol_table.set(self.children[0], node[0], node[1])
                
            else: 
                # print("atempting to put: ", self.value, self.children, " in symbol table")
                symbol_table.set(self.children[0], "int", 7)

#Nodes.FuncDec("FuncDec", [varDec, variables, block])
class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self, symbol_table):
        # print("in funcDec")
        name = self.children[0].children[0].value
        type = self.children[0].value.value
        node = self

        # print("name: ", name)
        # print("type: ", type)
        # print("node: ", node)

        funcTable.set(name, type, node)
        # print("saved in func table: ",  name, funcTable.get(name))

#Nodes.FuncCall(identifier.value, [identifier.value, assingments])
#TODO -> parece que quando ele volta pro evaluate da main, ele comeca do comeco? e nao de onde parou??
class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("in funcCall")
        # print("funcTable: ", self.value)
        func = funcTable.get(self.value)
        type = func[0]
        dec = func[1]
        varDec = dec.children[0]
        children = dec.children[1]
        block = dec.children[2]

        # print("evaluating my own children: ", self.children)
        func_call_children = []
        new_table = SymbolTable()

        # print("evaluating the FunDec children: ", children)
        func_dec_child_names = []
        for child in children:
            # print("funcDec child:", child.children[0].value)
            func_dec_child_names.append(child.children[0].value)
            child.evaluate(new_table)
        # print("child_names: ", func_dec_child_names)

        for child in self.children[1]:
            # print("child: ", child)

            if isinstance(child, list) == "list":
                func_call_children.append(child.children[1].evaluate(symbol_table))
            elif child: 
                func_call_children.append(child.evaluate(symbol_table))

            # func_call_children.append(child.children[1].evaluate(symbol_table))
            # func_call_children.append(child.children[1].value)
            # print(func_call_children)

        if func_call_children and children:

            if len(func_dec_child_names) != len(func_call_children):
                raise Exception("Wrong number of arguments")
    
            for i in range(len(func_call_children)):
                # print("child:", func_dec_child_names[i], func_call_children[i][0], func_call_children[i][1])
                # funcTable.set(func_dec_child_names[i], func_call_children[i][0], func_call_children[i][1])
                new_table.set(func_dec_child_names[i], func_call_children[i][0], func_call_children[i][1])


        # print("debug func_table: ", funcTable.table)
        # print("debug symbol_table: ", symbol_table.table)
        # print("debug new_table: ", new_table.table)


        #TODO - mudar para corretamente checar os tipos
        # for i in range(len(func_dec_child_names)):
        #     if func_dec_child_names[i] != func_call_child_names[i]:
        #         raise Exception("Wrong argument type")

        if self.value == 'main':
            block.evaluate(symbol_table)

        else: 
            result = block.evaluate(new_table)
            # print("debug func_table: ", funcTable.table)
            # print("debug symbol_table: ", symbol_table.table)
            # print("debug new_table: ", new_table.table)
            # print("funcCall result: ", result)
            return result
            

class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print("in return")
        # print("children: ", self.children[0].value)
        # print("retuning: ", self.children[0].evaluate(symbol_table))
        return self.children[0].evaluate(symbol_table)

        
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

    #value == type, children[0] == identifier, children[1] == value
    def evaluate(self, symbol_table):
        # print("varDec Node: ", self.value.value, self.children[0].value)

        if symbol_table.isIn(self.children[0].value):
            raise Exception("Syntax Error")

        if self.children[1] is not None:
            node = self.children[1].evaluate(symbol_table)

            if self.value == "int":
                if isinstance(node[1], str):
                    raise Exception("Syntax Error")

            if self.value == "string":
                if isinstance(node[1], int) or isinstance(node[1], float):
                    raise Exception("Syntax Error")
                
            symbol_table.set(self.children[0].value, self.value, node[1])
            
        else: 
            # print("atempting to put: ", self.value.value, self.children[0].value, " in symbol table")
            symbol_table.set(self.children[0].value, self.value.value, self.children[0].value)

        # return(self.children[0].value, self.children[1].evaluate(symbol_table))

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return ("int", self.value)
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        return ("string", self.value)
    
class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        # print(self.children)
        # print(self.children[0])
        child_0 = self.children[0].evaluate(symbol_table)
        child_1 = self.children[1].evaluate(symbol_table)

        # print("child_0 is type node?: ", isinstance(child_0[0], Type))

        if isinstance(child_0[0], Type):
            child_0 = list(child_0)
            child_0[0] = child_0[0].evaluate(symbol_table)
            if child_0[0] == 'i':
                child_0[0] = "int"

            child_0 = tuple(child_0)

        # print("child_0: ", child_0[0])
        # print("child_1: ", child_1[0])

        if child_0[0] != child_1[0] and (self.value != "."):
            raise Exception("Syntax Error")

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
                return ("string", str(child_0[1]) + str(child_1[1]))

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
