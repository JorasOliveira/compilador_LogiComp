import sys
from Parser import Parser
from comment_filter import comment_filter



def main():
    code = comment_filter(sys.argv[1])
    print(Parser.run(code).evaluate())


if __name__ == "__main__":
    main()
