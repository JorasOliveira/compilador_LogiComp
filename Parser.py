import Tokenizer
import Nodes

class Parser:
    def parse_program(tokenizer):
        result = Nodes.Block("Block",[])
        
        while tokenizer.next.type != "none":
            thing = Parser.parse_statement(tokenizer)

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

                while (tokenizer.next.type != "none") and (tokenizer.next.value != "}"):
                    thing = Parser.parse_statement(tokenizer)

                    if thing != None:
                        result.children.append(thing)

                    tokenizer.select_next()

                if tokenizer.next.value == "}":
                    tokenizer.select_next()
                    return result
        
    def parse_statement(tokenizer):
        
        while tokenizer.next.type == "newline":
            tokenizer.select_next()
        
        if tokenizer.next.type == "identifier":
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
                   
        elif tokenizer.next.value == "if":
           
            tokenizer.select_next()
            expression = Parser.bool_expression(tokenizer)
            block = Parser.parse_block(tokenizer)

            if tokenizer.next.type == "else":
                tokenizer.select_next()
                block2 = Parser.parse_block(tokenizer)
                return Nodes.Else("else", [expression, block, block2])   
                
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

        elif (tokenizer.next.value in ["{", "}"]) or isinstance(tokenizer.next.value, int): raise Exception("incorrect sintax")

    def parse_assingment(tokenizer):
        if tokenizer.next.type == "identifier":
            identifier = Nodes.Identifier(tokenizer.next.value)
            tokenizer.select_next()
            

            if tokenizer.next.value == "=":
                tokenizer.select_next()
                symbol = Parser.bool_expression(tokenizer)
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
        
        if tokenizer.next.type == "scanln":
            tokenizer.select_next()
            if tokenizer.next.type == "open_par":
                result = input()
                result = Nodes.IntVal(int(result))

            tokenizer.select_next()

            if tokenizer.next.type == "close_par":
                tokenizer.select_next()
                return result

            # raise Exception("Unbalanced parentheses: '(' without ')'")


        elif tokenizer.next.type == "number" or tokenizer.next.type == "identifier":

            if tokenizer.next.type == "identifier":
                node = Nodes.Identifier(tokenizer.next.value)

            else: node = Nodes.IntVal(tokenizer.next.value)

            tokenizer.select_next()
            if (tokenizer.next.value.isalpha()): raise Exception("incorrect sintax")
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
            right_operand = Parser.parse_expression(tokenizer) 
            result = Nodes.BinOp(operator, [result, right_operand])
        return result

    def bool_term(tokenizer):
        result = Parser.rel_expression(tokenizer)

        if tokenizer.next.value == "&&":
            tokenizer.select_next()
            right_operand = Parser.bool_term(tokenizer)
            result = Nodes.BinOp("&&", [result, right_operand])
        return result

    def bool_expression(tokenizer):
        result = Parser.bool_term(tokenizer)

        if tokenizer.next.value == "||":
            tokenizer.select_next()
            right_operand = Parser.bool_expression(tokenizer) 
            result = Nodes.BinOp("||", [result, right_operand])
        return result
    
    def run(code):
        tokenizer = Tokenizer.Tokenizer(code, 0)
        tokenizer.select_next()
        result = Parser.parse_program(tokenizer)

        if tokenizer.open_parentheses_count != 0:
            raise Exception("incorrect number of parentheses")

        return result