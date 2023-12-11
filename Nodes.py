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

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
                       
        ebp = symbol_table.get_ebp(self.children[0]) 
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

            writer(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return \n")    
            symbol_table.set(self.children[0], node[0], node[1], ebp)
            
        else:   
            writer(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return\n") 
            symbol_table.set(self.children[0], self.value, self.children[1], ebp)
        
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        value = symbol_table.get(self.value)
        ebp = symbol_table.get_ebp(self.value) 
        writer(f"MOV EAX, [EBP {ebp}]; resultado da atribuição\n") #f"MOV EAX, {value[1]} ; Evaluate() do filho da direita\n" +
        
        return value

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if isinstance(self.children[0], int):
            result = self.children[0]
            if result != None:
                writer( "MOV EAX, [EBP -4] ; Evaluate do Identifier, único filho do print\n" +
                        "PUSH EAX ; Empilha os argumentos para chamar a funcao\n" +
                        "PUSH formatout ; Dizendo para o printf que é um inteiro\n" +
                        "CALL printf ; Chamada da função\n" +
                        "ADD ESP, 8 ; Remove os argumentos da pilha\n")
                
                print(result[1])

        else:
            result = self.children[0].evaluate(symbol_table)
            if result != None:
                writer("MOV EAX, [EBP -4] ; Evaluate do Identifier, único filho do print\n" +
                        "PUSH EAX ; Empilha os argumentos para chamar a funcao\n" +
                        "PUSH formatout ; Dizendo para o printf que é um inteiro\n" +
                        "CALL printf ; Chamada da função\n" +
                        "ADD ESP, 8 ; Remove os argumentos da pilha\n") 
                   
                print(result[1])

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        self.unique_id = id(self)

    def evaluate(self, symbol_table):
        condition = self.children[0].evaluate(symbol_table)
        writer("CMP EAX, False; Evaluate do If\n")

        if condition[1]:
            self.children[1].evaluate(symbol_table)
            writer("CALL binop_true\n")
            writer(f"JE end_if{str(self.unique_id)[0:4]} ; Jump pro final do if\n")

        writer("CALL binop_false\n")
        writer(f"end_if{str(self.unique_id)[0:4]}: ; Fim do if\n")


class Else(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        self.unique_id = id(self)

    def evaluate(self, symbol_table):
        writer("CMP EAX, False; Evaluate do If\n")
        writer(f"JE else_{str(self.unique_id)[0:4]} ; Jump pro final do if\n") 

        if self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)[1]
            writer("CALL binop_true\n")
            writer(f"JMP end_if_else{str(self.unique_id)[0:4]} ; Jump pro final do if\n")
        else:
            writer(f"else_{str(self.unique_id)[0:4]}: ;\n")
            self.children[2].evaluate(symbol_table)
            writer("CALL binop_false\n")

        writer(f"end_if_else{str(self.unique_id)[0:4]}: ; Fim do if\n")

class For(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        self.unique_id = id(self)
    
    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)

        end_loop = f"EXIT_{str(self.unique_id)[0:4]}"

        writer(f"LOOP_{str(self.unique_id)[0:4]}:\n")
        
        # while self.children[1].evaluate(symbol_table)[1]:
        
            # writer("CMP EAX, False\n")
            # writer("CALL binop_je\n")
            # writer(f"JMP {end_loop}\n")
        self.children[1].evaluate(symbol_table)[1]
        writer(f'CMP EAX, False\nJE EXIT_LOOP_{str(self.unique_id)[0:4]}\n')
        self.children[3].evaluate(symbol_table)
        self.children[2].evaluate(symbol_table)
        # writer(f"JMP LOOP_{str(self.unique_id)[0:4]}\n")
        writer(f'JMP LOOP_{str(self.unique_id)[0:4]}\nEXIT_LOOP_{str(self.unique_id)[0:4]}:\n')

        # writer(f"{end_loop}:\n")

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
        
        writer("PUSH DWORD 0 ; alocação na primeira atribuição\n")

        if self.children[1] is not None:
            node = self.children[1].evaluate(symbol_table)

            if self.value == "int":
                if isinstance(node[1], str):
                    raise Exception("Syntax Error")

            if self.value == "string":
                if isinstance(node[1], int) or isinstance(node[1], float):
                    raise Exception("Syntax Error")

            # ebp = symbol_table.get_ebp(self.children[0].value)   
            ebp = symbol_table.get_len() * -4
            # print("ebp: ", ebp)

            writer(f"MOV [EBP {ebp}], EAX; resultado da atribuição - não há return\n") 
            symbol_table.set(self.children[0].value, self.value, node[1], ebp - 4)
            
        else: 
            # ebp = symbol_table.get_ebp(self.children[0].value) 
            ebp = symbol_table.get_len() * -4
            symbol_table.set(self.children[0].value, self.value.value, self.children[0].value, ebp -4)

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        writer(f"MOV EAX, {self.value}; Evaluate do IntVal\n")
        return ("int", self.value)
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        writer("MOV EAX, " + str(self.value) + " ; Evaluate do StrVal\n")
        return ("string", self.value)
    
class ScanLn(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbol_table):
        result = input()

        writer("; Scanln\n" + 
                "PUSH scanint ; endereço de memória de suporte\n" +
                "PUSH formatin ; formato de entrada (int)\n" +
                "CALL scanf\n" + 
                "ADD ESP, 8 ; Remove os argumentos da pilha\n" + 
                "MOV EAX, DWORD [scanint] ; retorna o valor lido em EAX\n" +
                "MOV [EBP -4], EAX; resultado da atribuição\n")
        
        return ("int", int(result))
    
class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        child_1 = self.children[1].evaluate(symbol_table)

        writer("PUSH EAX ; O BinOp guarda o resultado na pilha\n")

        child_0 = self.children[0].evaluate(symbol_table)

        if isinstance(child_0[0], Type):
            child_0 = list(child_0)
            child_0[0] = child_0[0].evaluate(symbol_table)
            if child_0[0] == 'i':
                child_0[0] = "int"

            child_0 = tuple(child_0)

        writer("POP EBX ; O BinOp recupera o valor da pilha em EAX\n")

        if child_0[0] != child_1[0] and (self.value != "."):
            raise Exception("Syntax Error")

        if child_0 != None and child_1 != None:
            if self.value == "+":
                writer("ADD EAX, EBX ;\n")
                return ("int", child_0[1] + child_1[1])
            if self.value == "-":
                writer("SUB EAX, EBX ;\n")
                return ("int", child_0[1] - child_1[1])
            if self.value == "*":
                writer("IMUL EBX ;\n")
                return ("int", child_0[1] * child_1[1])
            if self.value == "/":
                writer("IDIV EBX ;\n")
                return ("int", child_0[1] // child_1[1])
            
            #because of go, we return 1 or 0 for booleans
            if self.value == '||':
                writer("OR EAX, EBX ;\n")
                if child_0[1] or child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)

            if self.value == "&&":
                writer("AND EAX, EBX ;\n")
                if child_0[1] and child_1[1]:
                    return ("int", 1)
                else: return ("int", 0)

            if self.value == "==":
                writer("CMP EAX, EBX\n" +
                       "CALL binop_je\n")
                if (child_0[1] == child_1[1]):
                    return ("int", 1)
                else: 
                    return ("int", 0) 
                
            if self.value == ">":
                writer("CMP EAX, EBX\n"+
                       "CALL binop_jg\n")
                if child_0[1] > child_1[1]:
                    return ("int", 1)
                else: 
                    return ("int", 0)
                
            if self.value == "<":
                writer("CMP EAX, EBX\n" +
                       "CALL binop_jl\n")
                if child_0[1] < child_1[1]:
                    return ("int", 1)
                else: 
                    return ("int", 0)
                
            if self.value == ".":
                return ("string", str(child_0[1]) + str(child_1[1]))

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "+":
            writer(f"MOV EAX, {self.children[0].evaluate(symbol_table)[1]}\n")
            return ("int", self.children[0].evaluate(symbol_table)[1])

        if self.value == "-":
            writer("NEG EAX\n")
            return ("int", - self.children[0].evaluate(symbol_table)[1])
        
        if self.value == "!":
            writer(f"MOV EAX, {not self.children[0]}\n")
            return ("int",  not self.children[0])

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, symbol_table):
        return None

def header():
    with open("header.txt", "r") as f:
        h = f.read()
    with open("teste1.asm", "w") as f:
        f.write(h)

def writer(code):
    with open("teste1.asm", "a") as f:
        f.write(code)
    with open("teste1.asm", "a") as f:
        f.write("\n")
def footer():
    with open("footer.txt", "r") as f:
        h = f.read()
    with open("teste1.asm", "a") as f:
        f.write(h)