import sys
import re


strings = sys.argv[1:] #get all arguments except the first one (the file name)

args = []
numbers = []

char_numbers = ['1','2','3','4','5','6','7','8','9','0'] #list to compare the input chars with
ok_chars = ['+','-',' ','\n','\t',''] #list to compare the input chars with

temp_chars = []


for str in strings:
    for char in str:
        if char in char_numbers:
            temp_chars.append(char)
        
        elif char not in ok_chars:
            # continue
            print("char: " + char)
            raise Exception("wrong input")

        if char == '+':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            temp_chars = []

        if char == '-':
            args.append(char)
            numbers.append(int(''.join(temp_chars)))
            temp_chars = []
        


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


# print('------------------')
# print(args)
# print(numbers)
print(result)
