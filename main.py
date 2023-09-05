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
    

    #refazer pois esta uma caca
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

            elif self.source[self.position] in  ['+', '-', '*', '/']:

                self.next = Token('operator', self.source[self.position])
                self.position += 1

            elif self.source[self.position] == '(':

                self.next = Token('open_par', self.source[self.position])
                self.position += 1

            elif self.source[self.position] == ')':

                self.next = Token('close_par', self.source[self.position])
                self.position += 1

            else: raise Exception("Invalid character: " + self.source[self.position])

        else: self.next = None  # No more tokens

class Parser:

    def parse_factor(tokenizer):
        result = 0
        
        if tokenizer.next.value == '+':
            tokenizer.select_next()
            return Parser.parse_factor(tokenizer)

        elif tokenizer.next.value == '-':
            tokenizer.select_next()
            return (-1) * Parser.parse_factor(tokenizer)

        elif tokenizer.next != None and tokenizer.next.value == '(':
            
            tokenizer.select_next()
            result = Parser.parse_expression(tokenizer)

            if tokenizer.next != None and tokenizer.next.value == ')':
                tokenizer.select_next()
                return result 

            else: raise Exception("wrong input 3")


        if tokenizer.next.type == 'number':
            result = tokenizer.next.value
            tokenizer.select_next()
            return result

            if tokenizer.next == None: 
                raise Exception("wrong input 5")

        else: raise Exception("wrong input 4")

    def parse_term(tokenizer):
        result = Parser.parse_factor(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ['*', '/']:
            
            if tokenizer.next.value == '*':
                tokenizer.select_next()
                
                result *= Parser.parse_factor(tokenizer)
                # if tokenizer.next.type == 'number':
                #     result *= tokenizer.next.value
                    
                # else: raise Exception("wrong input 1")

            elif tokenizer.next.value == '/':
                tokenizer.select_next()

                result //= Parser.parse_factor(tokenizer)

                # if tokenizer.next.type == 'number':
                #     result //= tokenizer.next.value

                # else: raise Exception("wrong input 2")

            tokenizer.select_next()

        return result

    def parse_expression(tokenizer):
        result = Parser.parse_term(tokenizer)

        while tokenizer.next != None and tokenizer.next.value in ['+', '-']: 

            if tokenizer.next.value == '+' and tokenizer.next != None:
                tokenizer.select_next()
                result += Parser.parse_term(tokenizer)

            elif tokenizer.next.value == '-' and tokenizer.next != None:
                tokenizer.select_next()
                result -= Parser.parse_term(tokenizer)

        return result   

    

    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.select_next()

        return Parser.parse_expression(tokenizer)
    
def main():
    print(Parser.run(sys.argv[1]))


if __name__ == '__main__':
    main()






