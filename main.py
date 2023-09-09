import sys

class Token:
    def __init__(self, type, value):
        self.type = type  #str
        self.value = value #int

class Tokenizer:
    def __init__(self, source, position):
        self.source = source #str
        self.position = position #int
        self.next = Token("none", 0) #token
        self.open_parentheses_count = 0  # Keep track of open parentheses

    def select_next(self):
        if self.position < len(self.source):

            while self.source[self.position] in [' ', '\n', '\t']:
                self.position += 1

            if self.source[self.position].isdigit() and self.next.type != 'number':

                end_index = self.position
                while end_index < len(self.source) and self.source[end_index].isdigit():
                    end_index += 1

                number_str = self.source[self.position:end_index]
                self.next = Token('number', int(number_str))
                self.position = end_index

            elif self.source[self.position] in ['+', '-', '*', '/']:
                self.next = Token('operator', self.source[self.position])
                self.position += 1

            elif self.source[self.position] == '(':
                self.open_parentheses_count += 1  # Increment open parentheses count
                self.next = Token('open_par', self.source[self.position])
                self.position += 1

            elif self.source[self.position] == ')':

                if self.open_parentheses_count <= 0:
                    raise Exception("Unbalanced parentheses: ')' without '('")

                self.open_parentheses_count -= 1  # Decrement open parentheses count
                self.next = Token('close_par', self.source[self.position])
                self.position += 1

            else:
                raise Exception("Invalid character: " + self.source[self.position])

class Parser:

    def parse_factor(tokenizer):
        result = 0
        
        if tokenizer.next.value == '+':
            tokenizer.select_next()
            return Parser.parse_factor(tokenizer)

        if tokenizer.next.value == '-':
            tokenizer.select_next()
            return -Parser.parse_factor(tokenizer)

        if tokenizer.next.value == '(':
            tokenizer.select_next()
            result = Parser.parse_expression(tokenizer)

            if tokenizer.next.value == ')':
                tokenizer.select_next()
                return result

            raise Exception("Unbalanced parentheses: '(' without ')'")
        
        if tokenizer.next.type == 'number':
            result = tokenizer.next.value
            tokenizer.select_next()
            return result

        raise Exception("Invalid input")

    def parse_term(tokenizer):
        result = Parser.parse_factor(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ['*', '/']:
            
            if tokenizer.next.value == '*':
                tokenizer.select_next()
                result *= Parser.parse_factor(tokenizer)
 
            elif tokenizer.next.value == '/':
                tokenizer.select_next()
                result //= Parser.parse_factor(tokenizer)

        return result

    def parse_expression(tokenizer):
        result = Parser.parse_term(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ['+', '-']: 

            if tokenizer.next.value == '+':
                tokenizer.select_next()
                result += Parser.parse_term(tokenizer)

            elif tokenizer.next.value == '-':
                tokenizer.select_next()
                result -= Parser.parse_term(tokenizer)




        return result   

    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.select_next()

        result = Parser.parse_expression(tokenizer)

        if tokenizer.open_parentheses_count != 0:
            raise Exception("incorrect number of parentheses")

        return result
    
def main():
    print(Parser.run(sys.argv[1]))


if __name__ == '__main__':
    main()






