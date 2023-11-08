import sys
from Parser import Parser
from file_reader import read_file
from SymbolTable import SymbolTable



def main():
    code = read_file(sys.argv[1])
    symbol_table = SymbolTable()
    Parser.run(code).evaluate(symbol_table)



if __name__ == "__main__":
    main()
