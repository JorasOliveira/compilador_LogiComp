import sys


#strings = sys.argv[1:] #get all arguments except the first one (the file name)
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
            next_token = self.source[self.position]

            while next_token in [' ', '\n', '\t']:
                self.position += 1
                if self.position < len(self.source):
                    next_token = self.source[self.position]
                else:
                    break

            if next_token.isdigit():
                end_index = self.position
                while end_index < len(self.source) and self.source[end_index].isdigit():
                    end_index += 1

                number_str = self.source[self.position:end_index]
                self.next = Token('number', int(number_str))
                self.position = end_index

            elif next_token in ['+', '-']:
                self.next = Token('operator', next_token)
                self.position += 1

            else:
                raise Exception("Invalid character: " + next_token)
        else:
            self.next = None  # No more tokens

class Parser:
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.select_next()

        return Parser.parse_expression(tokenizer)

    def parse_expression(tokenizer):
        result = 0

        if tokenizer.next.type == 'number':

            result = tokenizer.next.value
            tokenizer.select_next()
            next_token = tokenizer.next.value

            if next_token in ['+', '-']:

                while next_token in ['+', '-']:

                    if tokenizer.next.value == '+':
                        tokenizer.select_next()
                        next_token = tokenizer.next

                        if next_token.type == 'number':
                            result += next_token.value

                        else: raise Exception("wrong input")

                    elif tokenizer.next.value == '-':
                        tokenizer.select_next()
                        next_token = tokenizer.next

                        if next_token.type == 'number':
                            result -= next_token.value

                        else: raise Exception("wrong input")

                    tokenizer.select_next()
                    # tokenizer.select_next()


                    if tokenizer.next is not None: 
                        next_token = tokenizer.next.value
            else: 
                raise Exception("wrong input")

            return result
        else: raise Exception("wrong input")
    

    
def main():
    print(Parser.run(sys.argv[1]))


if __name__ == '__main__':
    main()