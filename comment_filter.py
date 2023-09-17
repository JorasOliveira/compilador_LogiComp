def comment_filter(input_string):
    # Split the input string into lines
    lines = input_string.split('\n')
    
    # Initialize an empty list to store the lines without comments
    lines_without_comments = []
    
    for line in lines:
        # Check if the line contains '//' and remove everything after it
        if '//' in line:
            line = line[:line.index('//')]
        
        # Append the modified line (without comments) to the list
        lines_without_comments.append(line)
    
    # Join the modified lines to create the result string
    result_string = '\n'.join(lines_without_comments)
    
    return result_string
