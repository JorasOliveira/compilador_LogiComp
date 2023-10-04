import Tokenizer
import Nodes

class Parser:
    def parse_program(tokenizer):
        result = Nodes.Block("Block",[])
        
        while tokenizer.next.type != "none":
            thing = Parser.parse_statement(tokenizer)
            # print("thing: ", thing)

            if thing != None:
                result.children.append(thing)

            tokenizer.select_next()
        return result
    
    def parse_block(tokenizer):
        result = Nodes.Block("Block",[])

        if tokenizer.next.value == "{":
            tokenizer.select_next()

            if tokenizer.next.value == "\n":
                tokenizer.select_next()

                while tokenizer.next.type != "none":
                    thing = Parser.parse_statement(tokenizer)

                    if thing != None:
                        result.children.append(thing)

                    tokenizer.select_next()

            else: raise Exception("incorrect sintax")

            if tokenizer.next.value == "}":
                return result
            
        # raise Exception("incorrect sintax")

    def parse_statement(tokenizer): #TODO -> implementar o if and for aqui
        print("parse_statement: ", tokenizer.next.value)
        while tokenizer.next.type == "newline":
            tokenizer.select_next()
        
        if tokenizer.next.type == "identifier" and (tokenizer.next.value not in ["if", "for", "else"]):
            identifier = Parser.parse_assingment(tokenizer)
            return identifier
        
        if tokenizer.next.type == "println":
            tokenizer.select_next()

            if tokenizer.next.type == "open_par":
                tokenizer.select_next()
                expression = Parser.bool_expression(tokenizer)

                if tokenizer.next.type == "close_par":
                    tokenizer.select_next()
                    return Nodes.Print("Println", [expression])

        #TODO -> checar se esta tudo certo aqui       
        elif tokenizer.next.value == "if":
           
            tokenizer.select_next()
            expression = Parser.bool_expression(tokenizer)
            print("expression: ", expression)
            print("token value inside if: ", tokenizer.next.value)
            print(1)

            block = Parser.parse_block(tokenizer)

            if tokenizer.next.type == "else":
                print(2)
                tokenizer.select_next()
                block2 = Parser.parse_block(tokenizer)
                return Nodes.Else("If", [expression, block, block2])
            print(3)        
            return Nodes.If("If", [expression, block])
                
        elif tokenizer.next.value == "for":
            tokenizer.select_next()
            assingment = Parser.parse_assingment(tokenizer)

            if tokenizer.next.type == "semicolon":
                tokenizer.select_next()
                expression = Parser.bool_expression(tokenizer)

                if tokenizer.next.type == "semicolon":
                    tokenizer.select_next()
                    assingment2 = Parser.parse_assingment(tokenizer)
                    block = Parser.parse_block(tokenizer)
                    return Nodes.For("For", [assingment, expression, assingment2, block])

        elif (tokenizer.next.type == "newline") or isinstance(tokenizer.next.value, int): raise Exception("incorrect sintax")

    def parse_assingment(tokenizer):
        print("Token: ", tokenizer.next.value, " of type: ", tokenizer.next.type, ", parser assingment")

        if tokenizer.next.type == "identifier":
            identifier = Nodes.Identifier(tokenizer.next.value)
            tokenizer.select_next()

            if tokenizer.next.value == "=":
                tokenizer.select_next()
                symbol = Parser.bool_expression(tokenizer)
                #used to have a if tokenizer.next.type == "newline": tokenizer.select_next() + return here
                return Nodes.Assignment(identifier, [identifier.value, symbol])
            
        raise Exception("incorrect sintax")

    def parse_factor(tokenizer):
        result = 0

        if tokenizer.next.type == "operator":
            
            if tokenizer.next.value == "+":
                unit_op = Nodes.UnOp("+", [])
    
            if tokenizer.next.value == "-":
                unit_op = Nodes.UnOp("-", [])

            if tokenizer.next.value == "!":
                unit_op = Nodes.UnOp("!", [])

            tokenizer.select_next()
            unit_op.children.append(Parser.parse_factor(tokenizer))
            return unit_op

        if tokenizer.next.type == "open_par":
            tokenizer.select_next()
            result = Parser.bool_expression(tokenizer)

            if tokenizer.next.type == "close_par":
                tokenizer.select_next()
                return result

            raise Exception("Unbalanced parentheses: '(' without ')'")

        if tokenizer.next.type == "number" or tokenizer.next.type == "identifier":

            if tokenizer.next.type == "identifier":
                node = Nodes.Identifier(tokenizer.next.value)

            else: node = Nodes.IntVal(tokenizer.next.value)

            tokenizer.select_next()
            return node

    def parse_term(tokenizer):
        result = Parser.parse_factor(tokenizer)

        while tokenizer.next is not None and tokenizer.next.value in ["*", "/"]:
            operator = tokenizer.next.value
            tokenizer.select_next()
            right_operand = Parser.parse_factor(tokenizer)
            result = Nodes.BinOp(operator, [result, right_operand])

        return result

    def parse_expression(tokenizer):
        result = Parser.parse_term(tokenizer)
        while tokenizer.next is not None and tokenizer.next.value in ["+", "-"]:
            operator = tokenizer.next.value
            tokenizer.select_next()
            right_operand = Parser.parse_term(tokenizer)
            result = Nodes.BinOp(operator, [result, right_operand])

        return result
    
    def rel_expression(tokenizer):
        result = Parser.parse_expression(tokenizer)

        if tokenizer.next.value in ["<", ">", "=="]:
            operator = tokenizer.next.value
            tokenizer.select_next()
            right_operand = Parser.parse_expression(tokenizer) #coreto?
            result = Nodes.BinOp(operator, [result, right_operand])
        return result

    def bool_term(tokenizer):
        result = Parser.rel_expression(tokenizer)

        if tokenizer.next.value == "&&":
            tokenizer.select_next()
            right_operand = Parser.bool_term(tokenizer) #coreto?
            result = Nodes.BinOp("&&", [result, right_operand])
        return result

    def bool_expression(tokenizer):
        result = Parser.bool_term(tokenizer)

        if tokenizer.next.value == "||":
            tokenizer.select_next()
            right_operand = Parser.bool_expression(tokenizer) #Coreto?
            result = Nodes.BinOp("||", [result, right_operand])
        return result
    
    def run(code):
        tokenizer = Tokenizer.Tokenizer(code, 0)
        tokenizer.select_next()
        
        #TODO -> alterar para a chamada certa!
        result = Parser.parse_program(tokenizer)

        if tokenizer.open_parentheses_count != 0:
            raise Exception("incorrect number of parentheses")

        return result