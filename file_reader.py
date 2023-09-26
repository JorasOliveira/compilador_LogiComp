def read_file(filename):
    result_string = ''
    with open(filename, 'r') as file:
        for line in file:
            comment_index = line.find('//')

            if comment_index == 0:
                pass

            elif comment_index != -1:
                result_string += line[:comment_index] + '\n'

            else:
                result_string += line

        return result_string
    