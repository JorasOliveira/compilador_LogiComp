import Tokenizer
import Nodes

class Parser:

    def parse_statement(tokenizer):

        if tokenizer.next.type == "identifier":
            identifier = Nodes.Identifier(tokenizer.next.value)
            tokenizer.select_next()

            if tokenizer.next.value == "=":
                tokenizer.select_next()
                symbol = Parser.parse_expression(tokenizer)

                result = Nodes.Assignment(identifier, [identifier.value, symbol])
                return result
            
            return identifier
        
        elif tokenizer.next.type == "println":
            tokenizer.select_next()

            if tokenizer.next.type == "open_par":
                tokenizer.select_next()

                expression = Parser.parse_expression(tokenizer)

                if tokenizer.next.type == "close_par":
                    tokenizer.select_next()
                    result = Nodes.Print("Println", [expression])
                    return result
                
            else: raise Exception("incorrect sintax")

    def parse_block(tokenizer):
        result = Nodes.Block("Block",[])
        
        while tokenizer.next.type != "none":
            thing = Parser.parse_statement(tokenizer)

            if thing:
                result.children.append(thing)
                # print("appending: ", thing.value)

            tokenizer.select_next()
        return result

    def parse_factor(tokenizer):
        result = 0

        if tokenizer.next.type == "operator":
            
            if tokenizer.next.value == "+":
                unit_op = Nodes.UnOp("+", [])
    
            if tokenizer.next.value == "-":
                unit_op = Nodes.UnOp("-", [])

            tokenizer.select_next()
            unit_op.children.append(Parser.parse_factor(tokenizer))
            return unit_op

        if tokenizer.next.type == "open_par":
            tokenizer.select_next()
            result = Parser.parse_expression(tokenizer)


            if tokenizer.next.type == "close_par":
                tokenizer.select_next()
                return result

            raise Exception("Unbalanced parentheses: '(' without ')'")

        if tokenizer.next.type == "number" or tokenizer.next.type == "identifier":
            result = tokenizer.next.value
            # print("result at factor: ", result)

            number_node = Nodes.IntVal(result)
            tokenizer.select_next()
            return number_node

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
    
    def run(code):
        tokenizer = Tokenizer.Tokenizer(code, 0)
        tokenizer.select_next()
        
        result = Parser.parse_block(tokenizer)

        if tokenizer.open_parentheses_count != 0:
            raise Exception("incorrect number of parentheses")

        return result
    