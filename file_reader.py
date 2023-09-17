def read_file_content(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"