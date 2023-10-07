class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, identifier, node):
        identifier = identifier.strip()
        # print("putting: ", identifier, " in symbol table")

        if identifier == "Println":
            raise Exception("Incorrect Sintax")
        
        self.table[identifier] = node

    def get(self, identifier):

        identifier = identifier.strip()

        if identifier in self.table:
            result = self.table[identifier]

            if result:
                return result 
        
        else:
            raise KeyError(f"Identifier '{identifier}' not found in the symbol table.")