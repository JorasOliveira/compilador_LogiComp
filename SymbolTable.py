class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, identifier, node):
        identifier = identifier.strip()


        # print("adding key: ", identifier, " Value: ", node)

        if identifier == "Println":
            raise Exception("Incorrect Sintax")
        
        self.table[identifier] = node

    def get(self, identifier):

        identifier = identifier.strip()
        # print("atempting to get: ", identifier )  
        # print("current keys are: ", self.table.keys())  

        if identifier in self.table:
            result = self.table[identifier]
            # print("we got: ", result)

            if result:
                return result 
        
        else:
            raise KeyError(f"Identifier '{identifier}' not found in the symbol table.")