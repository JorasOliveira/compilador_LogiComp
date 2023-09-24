class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, identifier, node):
        identifier = identifier.strip()

        if identifier in self.table or node is None:
            pass

        else: 
            # print("adding key: ", identifier, " Value: ", node)
            self.table[identifier] = node

    def get(self, identifier):

        identifier = identifier.strip()    
        if identifier in self.table:
            result = self.table[identifier]

            if result:
                return result 
        
        else:
            raise KeyError(f"Identifier '{identifier}' not found in the symbol table.")