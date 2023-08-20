import sys


strings = sys.argv[1:] #get all arguments except the first one (the file name)

args = []
numbers = []

char_numbers = ['1','2','3','4','5','6','7','8','9','0'] #list to compare the input chars with
ok_chars = ['\n','\t','', ' '] #list to compare the input chars with
operators = ['+','-']

temp_chars = []
last_char = strings[0][0]

check_for_numbers = True
check_for_stupid_annoying_case = False

for str in strings:
    for char in str:
        if char in char_numbers:
            if check_for_stupid_annoying_case:
                raise Exception("wrong input")


            if last_char in char_numbers or last_char in operators or check_for_numbers:
                temp_chars.append(char)

        elif (char not in ok_chars) and (char not in operators):
            raise Exception("wrong input")
        

        if last_char in char_numbers and (char in ok_chars):
            check_for_stupid_annoying_case = True
            
        if char == '+':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            check_for_numbers = True
            check_for_stupid_annoying_case = False
            temp_chars = []

        if char == '-':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            check_for_numbers = True
            check_for_stupid_annoying_case = False
            temp_chars = []
        
        last_char = char


    numbers.append(int(''.join(temp_chars)))
    temp_chars = []


result = 0
for i in range(len(args)):
    if i == 0:
        result = numbers[i]

    if args[i] == '+':
        result += numbers[i+1]

    if args[i] == '-':
        result -=  numbers[i+1]

print(result)
