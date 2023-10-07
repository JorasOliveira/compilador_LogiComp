import Token
class Tokenizer:
    def __init__(self, source, position):
        self.source = source  # str
        self.position = position  # int
        self.next = Token.Token("none", 0)
        self.open_parentheses_count = 0  # Keep track of open parentheses

    def select_next(self):
        if self.position < len(self.source):
            # print("current token: " + str(self.next.value), "of type:", self.next.type)
            while self.source[self.position] in [" ", "\t"] and self.position < len(self.source): #passes white space
                self.position += 1

            if self.source[self.position] in ["+", "-", "*", "/", "<", ">", "!", "=", "|", "&"]: #tokenizes operators

                if self.source[self.position + 1] in ["=", "|", "&"]:
                    self.next = Token.Token("operator", self.source[self.position] + self.source[self.position + 1] )
                    self.position += 2

                else:
                    self.next = Token.Token("operator", self.source[self.position])
                    self.position += 1
                
            elif self.source[self.position].isdigit(): #Tokenizes full numbers
                end_index = self.position
                
                while end_index < len(self.source) and self.source[end_index].isdigit():
                    end_index += 1

                number_str = self.source[self.position : end_index]
                self.next = Token.Token("number", int(number_str))
                self.position = end_index
                    
            elif self.source[self.position].isalpha(): #tokenizes variable names
                end_index = self.position

                while (self.source[end_index] not in ["+", "-", "*", "/", "\n", "(", ")", "=", " ", "\n"]):
                    end_index += 1

                identifier_str = self.source[self.position : end_index]
                self.position = end_index

                if identifier_str == "Println":
                    self.next = Token.Token("println", identifier_str)

                elif identifier_str == "if":
                    self.next = Token.Token("if", identifier_str)
                
                elif identifier_str == "for":
                    self.next = Token.Token("for", identifier_str)
                
                elif identifier_str == "else":
                    self.next = Token.Token("else", identifier_str)

                elif identifier_str == ":=":
                    self.next = Token.Token("assingment", identifier_str)

                else:    
                    self.next = Token.Token("identifier", identifier_str)
                    
            #the next few are self explenatory, tokenizes the specied token
            elif self.source[self.position] == ";":
                self.next = Token.Token("semicolon", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "{":
                self.next = Token.Token("open_bracket", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "}":
                self.next = Token.Token("close_bracket", self.source[self.position])
                self.position += 1

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