class Lexer():
    def __init__(self):
        self._operators = ['+', '-', '*', '**', '/', '//', '%', '=', '+=', '-=', '/=', '*=', '%=', '//=', '**=', '==', '!=', '>', '>=', '<', '<=', 'and', 'or', 'not', 'in', 'not in']
        self._keywords = ['as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'for', 'from', 'if', 'import', 'None', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with']
        self._separators = [',', ';', ':', '(', ')', '{', '}', '[', ']']
        self._comments = ['#', '//', ]
        self._string = ['"', "'"]

        self.list_2 = []

        #self._file = list_1 
        #this opens up the file and separates the lines into a list
        try:
            with open("input_scode.txt") as f:
                self._file = f.readlines()
                #print(self._file)          #output is: ['while (t < upper) s = 22.00;\n', '\n', 'def test_case(n = 1):\n', '    return n - 2']
        except FileNotFoundError:
            print("File not found, ensure input_scode.txt is in directory")


    def run(self):
        for line in self._file:
            char_itr = 0
            single_char = line[char_itr]
            if single_char in self._comments or single_char == ' ': continue
            elif single_char == "'" or single_char == '"':
                starter = single_char
                self.list_2.append('separator')
                self.list_2.append(starter)
                self.list_2.append('string')
                char_itr += 1
                single_char = line[char_itr]
                while single_char != starter:
                    temp_string += single_char
                    char_itr += 1
                    single_char = line[char_itr]
                self.list_2.append(temp_string)
                char_itr += 1
                self.list_2.append('separator')
                self.list_2.append(line[char_itr])
                self.char_itr += 1
                    

def main():
    L = Lexer()
    L.run()

if __name__ == '__main__':
    main()