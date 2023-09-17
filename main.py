import sys
from Parser import Parser
from comment_filter import comment_filter
from file_reader import read_file_content



def main():
    code = read_file_content(sys.argv[1])
    code = comment_filter(code)
    print(Parser.run(code).evaluate())


if __name__ == "__main__":
    main()
