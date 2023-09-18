def comment_filter(input_string):
    # Split the input string into lines
    lines = input_string.split('\n')
    comment_index = 0
    for line in lines:
        # Check if the line contains '//' and remove everything after it
        if '//' in line:
            comment_index = line.index('//')
            break
    
    # Join the modified lines to create the result string
    result_string = input_string[:comment_index]
    print(result_string)
    
    return result_string
