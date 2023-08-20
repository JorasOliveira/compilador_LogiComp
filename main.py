import sys


strings = sys.argv[1:] #get all arguments except the first one (the file name)

args = []
numbers = []

char_numbers = ['1','2','3','4','5','6','7','8','9','0'] #list to compare the input chars with
ok_chars = ['+','-',' ','\n','\t',''] #list to compare the input chars with

temp_chars = []
last_char = strings[0][0]

# 1   -   22+333   +4


check_for_numbers = True

for str in strings:
    for char in str:
        if char in char_numbers:
            if last_char in char_numbers or last_char in ok_chars:
                temp_chars.append(char)

            else: 
                raise Exception("wrong input 1")

        
        elif char not in ok_chars:
            raise Exception("wrong input 2")
        

        if char == '+':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            check_for_numbers = True
            temp_chars = []

        if char == '-':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            check_for_numbers = True
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
