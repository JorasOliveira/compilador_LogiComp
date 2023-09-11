import sys
import Token
import Tokenizer
import Parser
import Nodes


def main():
    print(Parser.Parser.run(sys.argv[1]).evaluate())


if __name__ == "__main__":
    main()
