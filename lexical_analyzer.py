# Anne Edwards, Irvin Rafael, Joshua Villareal
operators = ['+', '-', '*', '**', '/', '//', '%', '=', '+=', '-=', '/=', '*=', '%=', '//=', '**=', '==', '!=', '>', '>=', '<', '<=', 'and', 'or', 'not', 'in']
keywords = ['as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'for', 'from', 'if', 'import', 'None', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with']
separators = [',', ';', ':', '(', ')', '{', '}', '[', ']']
comments = ['#', '//', ]
string = ['"', "'"]

class Lexer():
    def __init__(self):
        self.list = []
        self.file = []
       
    def open_file(self):
        try:
            with open("input_scode.txt") as f:
                self.file = f.readlines()
                print(self.file)          #output is: ['while (t < upper) s = 22.00;\n', '\n', 'def test_case(n = 1):\n', '    return n - 2']
        except FileNotFoundError:
            print("File not found, ensure input_scode.txt is in directory")
            
    def run(self):
        self.open_file()
        for line in self.file:
            # loop through the line
            self.char_iter = 0
            while self.char_iter < len(line):
                single_char = line[self.char_iter]
                # check to see if a space or beginning of a comment
                if single_char in comments or single_char == '\n':
                    break
                elif single_char == ' ':
                    self.char_iter += 1
                elif single_char == "'" or single_char == '"': # see if it's a string literal
                    starter = single_char
                    self.list.append('separator')
                    self.list.append(starter)
                    self.list.append('string')
                    self.char_iter += 1
                    single_char = line[self.char_iter]
                    temp_string = single_char
                    while single_char != starter:
                        temp_string += single_char
                        self.char_iter += 1
                        single_char = line[self.char_iter]
                    self.list.append(temp_string)
                    self.list.append('separator')
                    self.list.append(line[self.char_iter])
                    self.char_iter += 1
                elif self.test_if_constant(line=line): # see if it's an integer
                    self.list.append('constant')
                    self.list.append(str(self.constant))
                elif single_char in separators:
                    self.list.append('separator')
                    self.list.append(single_char)
                    self.char_iter += 1
                elif single_char in operators or single_char == 'a' or single_char == 'o' or single_char == 'i' or single_char == 'n': # +, -, *, /, =, ...
                    operator = single_char
                    two_op = single_char + line[self.char_iter + 1]
                    three_op = single_char + line[self.char_iter + 1] + line[self.char_iter + 2]

                    if three_op in operators:
                        self.char_iter += 3
                        operator = three_op
                    elif two_op in operators:
                        self.char_iter += 2
                        operator = two_op
                    
                    # handle 'word operators' (i.e and, or) 
                    if single_char == 'a' or single_char == 'n': # 'and' & 'not'
                        temp_operator = single_char + line[self.char_iter + 1] + line[self.char_iter + 2]
                        if temp_operator in operators:
                            self.char_iter += 3
                            operator = temp_operator
                    elif single_char == 'o' or single_char == 'i': # 'or' & 'in'
                        temp_operator = single_char + line[self.char_iter + 1]
                        if temp_operator in operators:
                            self.char_iter += 2
                            operator = temp_operator

                    if operator == single_char: # all other if/else failed
                        self.char_iter += 1

                    self.list.append('operator')
                    self.list.append(operator)
                else:
                    temp_string = single_char
                    self.char_iter += 1
                    s_char = line[self.char_iter]
                    if s_char == ' ':
                        pass
                    else:
                        while s_char not in separators and s_char not in operators and s_char not in comments and s_char != ' ' and s_char != '\n':
                            temp_string += s_char
                            self.char_iter += 1
                            s_char = line[self.char_iter]
                    
                    if temp_string in keywords:
                        self.list.append('keyword')
                    else:
                        self.list.append('identifier')
                    self.list.append(temp_string)

        # Print the list of tokens and lexemes
        print('Tokens          Lexemes')
        i = 0
        while i < (len(self.list) - 1):
            j = i + 1
            if len(self.list[i]) == 10:
                print(f'{self.list[i]}      {self.list[j]}')
            if len(self.list[i]) == 9:
                print(f'{self.list[i]}       {self.list[j]}')
            elif len(self.list[i]) == 8:
                print(f'{self.list[i]}        {self.list[j]}')
            elif len(self.list[i]) == 7:
                print(f'{self.list[i]}         {self.list[j]}')
            elif len(self.list[i]) == 6:
                print(f'{self.list[i]}          {self.list[j]}')
            i += 2

    def print_to_file(self):
        output = open("output.txt", 'w')
        output.write('Tokens          Lexemes\n')
        i = 0
        while i < (len(self.list) - 1):
            j = i + 1
            if len(self.list[i]) == 10:
                output.write(f'{self.list[i]}      {self.list[j]}\n')
            if len(self.list[i]) == 9:
                output.write(f'{self.list[i]}       {self.list[j]}\n')
            elif len(self.list[i]) == 8:
                output.write(f'{self.list[i]}        {self.list[j]}\n')
            elif len(self.list[i]) == 7:
                output.write(f'{self.list[i]}         {self.list[j]}\n')
            elif len(self.list[i]) == 6:
                output.write(f'{self.list[i]}          {self.list[j]}\n')
            i += 2
        output.close()

    def test_if_constant(self, line):
        num_iter = self.char_iter
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
        
        if len(possible_list) == 0:
            return False
        
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
        self.constant = float(constant_str)
        self.char_iter += iter
        return True
                    
def main():
    L = Lexer()
    L.run()
    L.print_to_file()


if __name__ == '__main__':
    main()
