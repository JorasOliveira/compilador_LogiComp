import Tokenizer
import Nodes


class Parser:
    def parse_factor(tokenizer):
        result = 0

        if tokenizer.next.type == "operator":
            
            if tokenizer.next.value == "+":
                unit_op_node = Nodes.UnOp("+", [])
    
            if tokenizer.next.value == "-":
                unit_op_node = Nodes.UnOp("-", [])

            tokenizer.select_next()
            unit_op_node.children.append(Parser.parse_factor(tokenizer))
            return unit_op_node

        if tokenizer.next.type == "open_par":
            tokenizer.select_next()
            result = Parser.parse_expression(tokenizer)


            if tokenizer.next.type == "close_par":
                tokenizer.select_next()
                return result

            raise Exception("Unbalanced parentheses: '(' without ')'")

        if tokenizer.next.type == "number":
            result = tokenizer.next.value

            number_node = Nodes.IntVal(result)
            
            tokenizer.select_next()
            return number_node

        raise Exception("Invalid input")

    def parse_term(tokenizer):
        result = Parser.parse_factor(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ["*", "/"]:
            if tokenizer.next.value == "*":
                bin_op = Nodes.BinOp("*", [])

            elif tokenizer.next.value == "/":
                bin_op = Nodes.BinOp("/", [])

            tokenizer.select_next()
            bin_op.children.append(result)
            bin_op.children.append(Parser.parse_factor(tokenizer))
            return bin_op

        return result

    def parse_expression(tokenizer):
        result = Parser.parse_term(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ["+", "-"]:
            if tokenizer.next.value == "+":
                bin_op = Nodes.BinOp("+", [])

            elif tokenizer.next.value == "-":
                bin_op = Nodes.BinOp("-", [])

            tokenizer.select_next()
            bin_op.children.append(result)
            bin_op.children.append(Parser.parse_term(tokenizer))
            return bin_op

        return result

    def run(code):
        tokenizer = Tokenizer.Tokenizer(code, 0)
        tokenizer.select_next()

        result = Parser.parse_expression(tokenizer)

        if tokenizer.open_parentheses_count != 0:
            raise Exception("incorrect number of parentheses")

        return result
