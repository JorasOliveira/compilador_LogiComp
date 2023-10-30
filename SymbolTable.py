class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, identifier, type, node):
        identifier = identifier.strip()
        if identifier == "Println":
            raise Exception("Incorrect Sintax")
        
        self.table[identifier] = (type, node)

    def get(self, identifier):

        identifier = identifier.strip()

        if identifier in self.table:
            result = self.table[identifier]
            return result 
        
        else:
            raise KeyError(f"Identifier '{identifier}' not found in the symbol table.")
    
    def isIn(self, identifier):
        identifier = identifier.strip()
        return identifier in self.table