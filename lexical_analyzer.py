# Anne Edwards, Irvin Rafael, Joshua Villareal
# CPSC 323-07
operators = ['+', '-', '*', '**', '/', '//', '%', '=', '+=', '-=', '/=', '*=', '%=', '//=', '**=', '==', '!=', '>', '>=', '<', '<=', 'and', 'or', 'not', 'in']
keywords = ['as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'for', 'from', 'if', 'import', 'None', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with']
separators = [',', ';', ':', '(', ')', '{', '}', '[', ']']
comments = ['#', '//', ]
string = ['"', "'"]

file = []

def open_file():
    try:
        with open("input_scode.txt") as f:
            file = f.readlines()
    except FileNotFoundError:
        print("File not found, ensure input_scode.txt is in directory")
    return file

def print_to_file(list):
        output = open("output.txt", 'w')
        output.write('Tokens          Lexemes\n')
        i = 0
        while i < (len(list) - 1):
            j = i + 1
            if len(list[i]) == 10:
                output.write(f'{list[i]}      {list[j]}\n')
            if len(list[i]) == 9:
                output.write(f'{list[i]}       {list[j]}\n')
            elif len(list[i]) == 8:
                output.write(f'{list[i]}        {list[j]}\n')
            elif len(list[i]) == 7:
                output.write(f'{list[i]}         {list[j]}\n')
            elif len(list[i]) == 6:
                output.write(f'{list[i]}          {list[j]}\n')
            i += 2
        output.close()

def test_if_keyword(single_char, line, char_iter):
    temp_list = []
    temp_string = single_char
    char_iter += 1
    iter = 1
    if char_iter >= len(line):
        pass
    else:
        s_char = line[char_iter]
        while s_char not in separators and s_char not in operators and s_char not in comments and s_char != ' ' and s_char != '\n':
            temp_string += s_char
            char_iter += 1
            iter += 1
            s_char = line[char_iter]

    category = ''
    if temp_string in keywords:
        category = 'keyword' 
    else:
        category = 'identifier'
    temp_list.append(category)
    temp_list.append(temp_string)

    return temp_list, iter

def test_if_constant(line, char_iter):
    num_iter = char_iter
    iter = 0
    possible_list = []
    while num_iter < len(line):
        if line[num_iter] in operators or line[num_iter] in separators:
            break
        elif line[num_iter] in comments or line[num_iter] == ' ' or line[num_iter] == '\n':
            break
        else:
            possible_list.append(line[num_iter])
        num_iter += 1
        iter += 1
    
    if len(possible_list) == 1: # only the first character was an integer
        constant = possible_list[0]
        iter = 1
        return constant, iter
    if len(possible_list) == 0:
        constant = None
        iter = 1
        return constant, iter
        
    j = 0
    constant_str = ''
    while j < len(possible_list):
        temp = possible_list[j]
        if temp == '.':
            constant_str += temp
        else:
            temp_num = ord(possible_list[j]) - 48
            if temp_num > 9:
                return False
            constant_str += possible_list[j]
        j += 1
    constant = constant_str
    return constant, iter

def lexer():
    list = []
    file = open_file()
    for line in file:
        char_iter = 0
        while char_iter < len(line):
            single_char = line[char_iter]
            if single_char in comments or single_char == '\n':
                break
            elif single_char == ' ':
                char_iter += 1
            elif single_char == "'" or single_char == '"': # see if it's a string literal
                starter = single_char
                list.append('separator')
                list.append(starter)
                list.append('string')
                char_iter += 1
                single_char = line[char_iter]
                temp_string = ''
                while single_char != starter:
                    temp_string += single_char
                    char_iter += 1
                    single_char = line[char_iter]
                list.append(temp_string)
                list.append('separator')
                list.append(line[char_iter])
                char_iter += 1
            elif single_char in separators:
                list.append('separator')
                list.append(single_char)
                char_iter += 1
            elif single_char in operators or single_char == 'a' or single_char == 'o' or single_char == 'i' or single_char == 'n': # +, -, *, /, =, ...
                operator = single_char

                # handle 'word operators' (i.e and, or) 
                if single_char == 'a' or single_char == 'n': # 'and' & 'not'
                    temp_operator = ''
                    s_char = single_char
                    iter = char_iter
                    while s_char not in separators and s_char not in comments and s_char != ' ' and s_char != '\n':
                        temp_operator += s_char
                        iter += 1
                        if iter >= len(line):
                            break
                        s_char = line[iter]

                    if temp_operator in operators:
                        char_iter += 3
                        operator = temp_operator
                    else:
                        temp, iter = test_if_keyword(single_char, line, char_iter)
                        list.append(temp[0])
                        list.append(temp[1])
                        char_iter += iter
                elif single_char == 'o' or single_char == 'i': # 'or' & 'in'
                    temp_operator = ''
                    s_char = single_char
                    iter = char_iter
                    while s_char not in separators and s_char not in comments and s_char != ' ' and s_char != '\n':
                        temp_operator += s_char
                        iter += 1
                        s_char = line[iter]
                    if temp_operator in operators:
                        char_iter += 2
                        operator = temp_operator
                    else:
                        temp, iter = test_if_keyword(single_char, line, char_iter)
                        list.append(temp[0])
                        list.append(temp[1])
                        char_iter += iter
                else:
                    two_op = single_char + line[char_iter + 1] # **, <=...
                    three_op = single_char + line[char_iter + 1] + line[char_iter + 2] # //= ...
                    if three_op in operators:
                        char_iter += 3
                        operator = three_op
                    elif two_op in operators:
                        char_iter += 2
                        operator = two_op

                if operator in operators: # final check
                    if operator == single_char:
                        char_iter += 1
                    list.append('operator')
                    list.append(operator)
            elif (ord(single_char) - 48) <= 9:
                constant, iter = test_if_constant(line=line, char_iter=char_iter)
                char_iter += iter
                if constant == None:
                    pass
                else:
                    list.append('constant')
                    list.append(constant)
            else:
                temp, iter = test_if_keyword(single_char, line, char_iter)
                char_iter += iter
                list.append(temp[0])
                list.append(temp[1])

    # Print the list of tokens and lexemes
    print('Tokens          Lexemes')
    i = 0
    while i < (len(list) - 1):
        j = i + 1
        if len(list[i]) == 10:
            print(f'{list[i]}      {list[j]}')
        if len(list[i]) == 9:
            print(f'{list[i]}       {list[j]}')
        elif len(list[i]) == 8:
            print(f'{list[i]}        {list[j]}')
        elif len(list[i]) == 7:
            print(f'{list[i]}         {list[j]}')
        elif len(list[i]) == 6:
            print(f'{list[i]}          {list[j]}')
        i += 2

    # Print to the file
    print_to_file(list)
                
def main():
    L = Lexer()
    L.run()

if __name__ == '__main__':
    main()
