import Token
class Tokenizer:
    def __init__(self, source, position):
        self.source = source  # str
        self.position = position  # int
        self.next = Token.Token("none", 0)
        self.open_parentheses_count = 0  # Keep track of open parentheses

    def select_next(self):
        if self.position < len(self.source):
            # print("current token: " + str(self.next.value), "of type: ", self.next.type)
            while self.source[self.position] in [" ", "\t"] and self.position < len(self.source):
                self.position += 1

            if self.source[self.position] in ["+", "-", "*", "/"]:
                self.next = Token.Token("operator", self.source[self.position])
                self.position += 1

            elif self.source[self.position].isdigit():
                end_index = self.position
                
                while end_index < len(self.source) and self.source[end_index].isdigit():
                    end_index += 1

                number_str = self.source[self.position : end_index]
                self.next = Token.Token("number", int(number_str))
                self.position = end_index

            elif self.source[self.position].isalpha():
                end_index = self.position

                while (self.source[end_index] not in ["+", "-", "*", "/", "\n", "(", ")", "="]):
                    end_index += 1

                identifier_str = self.source[self.position : end_index]
                self.position = end_index

                if identifier_str == "Println":
                    self.next = Token.Token("println", identifier_str)

                else:    
                    self.next = Token.Token("identifier", identifier_str)

            elif self.source[self.position] == "=":
                self.next = Token.Token("assingment", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "\n":
                self.next = Token.Token("newline", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "(":
                self.open_parentheses_count += 1  # Increment open parentheses count
                self.next = Token.Token("open_par", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == ")":
                if self.open_parentheses_count <= 0:
                    raise Exception("Unbalanced parentheses: ')' without '('")

                self.open_parentheses_count -= 1  # Decrement open parentheses count
                self.next = Token.Token("close_par", self.source[self.position])
                self.position += 1

            else:
                raise Exception("Invalid character: " + self.source[self.position])
            
        else: self.next = Token.Token("none", None)