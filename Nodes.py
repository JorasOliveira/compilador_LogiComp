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
        header()
        for child in self.children:
            child.evaluate(symbol_table)
        footer()

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
                       
        ebp = symbol_table.get_ebp() 
        ebp = ebp - 4  
        if self.children[1] is not None:
            node = self.children[1].evaluate(symbol_table)

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

            writter(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return \n")    
            symbol_table.set(self.children[0], node[0], node[1], ebp)
            
        # else:   
        #     writter(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return\n") 
        #     symbol_table.set(self.children[0], self.value, self.children[1], ebp)
        
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        value = symbol_table.get(self.value)

        writter("MOV [EBP -4], EAX; resultado da atribuição\n") #f"MOV EAX, {value[1]} ; Evaluate() do filho da direita\n" +
        
        return value

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if isinstance(self.children[0], int):
            result = self.children[0]
            if result != None:
                writter("MOV EAX, [EBP -4] ; Evaluate do Identifier, único filho do print\n" +
                        "PUSH EAX ; Empilha os argumentos para chamar a funcao\n" +
                        "PUSH formatout ; Dizendo para o printf que é um inteiro\n" +
                        "CALL printf ; Chamada da função\n" +
                        "ADD ESP, 8 ; Remove os argumentos da pilha")
                
                print(result[1])

        else:
            result = self.children[0].evaluate(symbol_table)
            if result != None:
                writter("MOV EAX, [EBP -4] ; Evaluate do Identifier, único filho do print\n" +
                        "PUSH EAX ; Empilha os argumentos para chamar a funcao\n" +
                        "PUSH formatout ; Dizendo para o printf que é um inteiro\n" +
                        "CALL printf ; Chamada da função\n" +
                        "ADD ESP, 8 ; Remove os argumentos da pilha") 
                   
                print(result[1])

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):

        condition = self.children[0].evaluate(symbol_table)
        # writter("CMP EAX, False; Evaluate do If\n")

        if condition[1]:
            self.children[1].evaluate(symbol_table)
            writter("CALL binop_true\n")
            return
            #writter("JMP end_if ; Jump pro final do if\n")
        writter("CALL binop_false\n")
        #writter("end_if: ; Fim do if\n")

class Else(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table): 
        if self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)[1]
            writter("CALL binop_true\n")
        else:
            self.children[2].evaluate(symbol_table)
            writter("CALL binop_false\n")

class For(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
#     def evaluate(self, symbol_table):

#         self.children[0].evaluate(symbol_table)
#         while self.children[1].evaluate(symbol_table)[1]:
            
#             self.children[3].evaluate(symbol_table)
#             self.children[2].evaluate(symbol_table)

    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)  
        loop_label = f"loop_label{id(self)}"
        end_loop = f"end_loop{id(self)}"
        writter(f"{loop_label}:\n")

        while self.children[1].evaluate(symbol_table)[1]:
            writter("CALL binop_je\n")
            writter(f"JMP {end_loop}\n")
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)  
            writter(f"JMP {loop_label}\n")

        writter(f"{end_loop}:\n")


class Type(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        
        # if symbol_table.isIn(self.children[0].value):
        #     raise Exception("Syntax Error")
        
        writter("PUSH DWORD 0 ; alocação na primeira atribuição\n")

        if self.children[1] is not None:
            node = self.children[1].evaluate(symbol_table)

            if self.value == "int":
                if isinstance(node[1], str):
                    raise Exception("Syntax Error")

            if self.value == "string":
                if isinstance(node[1], int) or isinstance(node[1], float):
                    raise Exception("Syntax Error")

            ebp = symbol_table.get_ebp()   

            writter(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return\n") 
            symbol_table.set(self.children[0].value, self.value, node[1], ebp - 4)
            
        else: 
            ebp = symbol_table.get_ebp()
            symbol_table.set(self.children[0].value, self.value.value, self.children[0].value, ebp)

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        writter(f"MOV EAX, {self.value} ; Evaluate do IntVal\n")
        return ("int", self.value)
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        writter("MOV EAX, " + str(self.value) + " ; Evaluate do StrVal\n")
        return ("string", self.value)
    
class ScanLn(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        result = input()

        writter("; Scanln\n" + 
                "PUSH scanint ; endereço de memória de suporte\n" +
                "PUSH formatin ; formato de entrada (int)\n" +
                "call scanf\n" + 
                "ADD ESP, 8 ; Remove os argumentos da pilha\n" + 
                "MOV EAX, DWORD [scanint] ; retorna o valor lido em EAX\n" +
                "MOV [EBP-4], EAX; resultado da atribuição\n")
        
        return ("int", int(result))
    
class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        child_1 = self.children[1].evaluate(symbol_table)

        writter("PUSH EAX ; O BinOp guarda o resultado na pilha\n")

        child_0 = self.children[0].evaluate(symbol_table)

        if isinstance(child_0[0], Type):
            child_0 = list(child_0)
            child_0[0] = child_0[0].evaluate(symbol_table)
            if child_0[0] == 'i':
                child_0[0] = "int"

            child_0 = tuple(child_0)

        writter("POP EBX ; O BinOp recupera o valor da pilha em EAX\n")

        if child_0[0] != child_1[0] and (self.value != "."):
            raise Exception("Syntax Error")

        if child_0 != None and child_1 != None:
            if self.value == "+":
                writter("ADD EAX, EBX ;\n")
                return ("int", child_0[1] + child_1[1])
            if self.value == "-":
                writter("SUB EAX, EBX ;\n")
                return ("int", child_0[1] - child_1[1])
            
            if self.value == "*":
                writter("IMUL EBX ;\n")
                return ("int", child_0[1] * child_1[1])
            if self.value == "/":
                writter("IDIV EBX ;\n")
                return ("int", child_0[1] // child_1[1])
            
            #because of go, we return 1 or 0 for booleans
            if self.value == '||':
                writter("OR EAX, EBX ;\n")
                if child_0[1] or child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)

            if self.value == "&&":
                writter("AND EAX, EBX ;\n")
                if child_0[1] and child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)

            if self.value == "==":
                if (child_0[1] == child_1[1]):
                    writter("CALL binop_je ;\n")
                    return ("int", 1)
                else: 
                    writter("CALL binop_false ;\n")
                    return ("int", 0) 
                
            if self.value == ">":
                if child_0[1] > child_1[1]:
                    writter("CALL binop_jg ;\n")
                    return ("int", 1)
                else: 
                    writter("CALL binop_jl ;\n")
                    return ("int", 0)
                
            if self.value == "<":
                if child_0[1] < child_1[1]:
                    writter("CALL binop_jl ;\n")
                    return ("int", 1)
                else: 
                    writter("CALL binop_jg ;\n")
                    return ("int", 0)
                
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

def header():
    f = open("header.txt", "r")
    h = f.read()
    f.close()
    f = open("teste1.asm", "w")
    f.write(h)
    f.close()

def writter(code):
    f = open("teste1.asm", "a")
    f.write(code)
    f.close()

def footer():
    f = open("footer.txt", "r")
    h = f.read()
    f.close()
    f = open("teste1.asm", "a")
    f.write(h)
    f.close()
