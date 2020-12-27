from collections import deque


class SmartCalculator():
    OPERATOR = '+-*/^()'
    map_priotity = {
        '-': 3,
        '+': 3,
        '*': 4,
        '/': 4,
        '^': 5,
    }

    def __init__(self):
        self.var_dict = {}
        self.postfix_out = deque()  # for postfix notation
        self.stack_oper = deque()  # stack for operand
        # self.result_oper = deque() # for calculate postfix notation
        self.oper_plus = None  # flag of operators, for func callculate
        self.flag_sucsess_check = True  # flag of sucsess chech input line
        self.inv_expres = 'Invalid expression'
        self.line = []

        while True:
            self.line_input = input()
            if self.line_input.startswith('/'):  # block for command, begin with '/'
                if self.line_input[1:] == 'exit':
                    self.exit_calc()
                elif self.line_input[1:] == 'help':
                    self.help_calc()
                else:
                    print('Unknown command')
            elif '=' in self.line_input:
                self.variable()
            elif self.line_input == '':
                continue
            else:
                self.evaluate_line()

    def evaluate_line(self):
        '''
        Code errors on flag_sucsess_check:
        0 - no errors
        1 - Invalid expression ()
        2 - Unkown variable
        '''
        self.flag_sucsess_check = 0
        self.check_line()
        if self.flag_sucsess_check == 0:
            self.postfix_quere()
            if self.flag_sucsess_check == 0:
                self.callculate()

        elif self.flag_sucsess_check == 1:
            print('Invalid expression')
        else:
            print('Invalid expression')

    def postfix_quere(self):  # transform line in reverse polish notation
        self.postfix_out.clear()
        self.stack_oper.clear()
        self.count = 0
        while True:
            try:
                self.value = self.line[self.count]
            except IndexError:
                while True:
                    try:
                        self.postfix_out.append(self.stack_oper.pop())
                    except IndexError:
                        break
                self.finish_to_postfix = True
                break
            else:
                if self.is_digit(self.value):
                    self.postfix_out.append(int(self.value))
                elif self.value in self.var_dict.keys():
                    self.postfix_out.append(self.var_dict[self.value])
                elif self.value in self.OPERATOR:
                    if self.value == '(':
                        self.stack_oper.append(self.value)
                    elif self.value == ')':
                        while True:
                            if self.stack_oper[-1] != '(':
                                self.postfix_out.append(self.stack_oper.pop())
                            elif self.stack_oper[-1] == '(':
                                self.stack_oper.pop()
                                break
                    elif len(self.stack_oper) == 0:
                        self.stack_oper.append(self.value)
                    else:
                        if self.stack_oper[-1] == '(':
                            self.stack_oper.append(self.value)
                        else:
                            if self.map_priotity[self.value] > self.map_priotity[self.stack_oper[-1]]:
                                self.stack_oper.append(self.value)
                            elif self.map_priotity[self.value] <= self.map_priotity[self.stack_oper[-1]]:
                                while True:
                                    try:
                                        self.stack_oper[-1]
                                    except IndexError:
                                        break
                                    else:
                                        if self.stack_oper[-1] == '(':
                                            break
                                        elif self.map_priotity[self.value] <= self.map_priotity[self.stack_oper[-1]]:
                                            self.postfix_out.append(self.stack_oper.pop())
                                        else:
                                            break
                                self.stack_oper.append(self.value)
                else:
                    print('Unknown variable')
                    self.flag_sucsess_check = 2
                    break
            self.count += 1

    def callculate(self):
        self.stack_oper.clear()
        while True:
            try:
                self.postfix_out[0]
            except IndexError:
                break
            else:
                if self.is_digit(self.postfix_out[0]):
                    self.stack_oper.append(self.postfix_out.popleft())
                elif self.postfix_out[0] in self.OPERATOR:
                    try:
                        self.second = self.stack_oper.pop()
                        self.first = self.stack_oper.pop()
                    except IndexError:
                        print('Invalid expression')
                        break
                    else:
                        if self.postfix_out[0] == '-':
                            self.stack_oper.append(self.first - self.second)
                        elif self.postfix_out[0] == '+':
                            self.stack_oper.append(self.first + self.second)
                        elif self.postfix_out[0] == '*':
                            self.stack_oper.append(self.first * self.second)
                        elif self.postfix_out[0] == '/':
                            self.stack_oper.append(self.first / self.second)
                        elif self.postfix_out[0] == '^':
                            self.stack_oper.append(self.first ** self.second)
                        self.postfix_out.popleft()
        print(self.if_int(self.stack_oper[0]))

    def check_line(self):
        self.line.clear()
        self.count = 0
        self.number = ''  # stack for number
        self.variable_name = ''  # stack for name variable
        self.operator_name = ''
        while True:
            try:
                self.line_input[self.count]
            except IndexError:
                if len(self.number) != 0:
                    self.line.append(self.number)
                    self.number = ''
                elif len(self.variable_name) != 0:
                    self.line.append(self.variable_name)
                    self.variable_name = ''
                break
            else:
                if self.line_input[self.count] in '0123456789.':
                    self.number += self.line_input[self.count]
                elif self.line_input[self.count].isalpha():
                    self.variable_name += self.line_input[self.count]
                elif self.line_input[self.count] in '-+*/^() ':

                    if self.line_input[self.count] in '-+*/^':
                        self.operator_name += self.line_input[self.count]

                    if len(self.number) != 0:
                        self.line.append(self.number)
                        self.number = ''
                    elif len(self.variable_name) != 0:
                        self.line.append(self.variable_name)
                        self.variable_name = ''

                    if self.line_input[self.count] != ' ':
                        self.line.append(self.line_input[self.count])
                    elif self.line_input[self.count] == ' ':
                        if len(self.operator_name) > 1:
                            self.flag_sucsess_check = 1
                            break
                        else:
                            self.operator_name = ''
            self.count += 1

        self.stack_oper.clear()
        for elem in self.line:
            if elem == '(':
                self.stack_oper.append(elem)
            elif elem == ')':
                try:
                    self.stack_oper.pop()
                except IndexError:
                    self.flag_sucsess_check = 1
                    break

        if len(self.stack_oper) != 0:
            self.flag_sucsess_check = 1

    def is_digit(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def if_int(self, digit):
        if int(digit) == digit:
            return int(digit)
        else:
            return digit

    def variable(self):  # check, set, update variable in var_dict
        if self.line_input.count('=') > 1:
            print('Invalid assignment')
        else:
            self.line_input = self.line_input.replace(' ', '')
            self.line_input = self.line_input.split('=')
            self.sym_var = self.line_input[0].strip()
            self.dig_var = self.line_input[1].strip()
            # test if slice witn name variable is symbol without number
            if not self.sym_var.isalpha():
                print('Invalid identifier')
            else:
                # check if value is symbol and variable
                if self.dig_var in self.var_dict.keys():
                    self.var_dict[self.sym_var] = self.var_dict[self.dig_var]
                # test if value variable is digit
                elif not self.dig_var.isdigit():
                    print('Invalid assignment')
                # if tests Ok< create variable
                else:
                    if self.dig_var.count('.') != 0:
                        self.var_dict[self.sym_var] = float(self.dig_var)
                    else:
                        self.var_dict[self.sym_var] = int(self.dig_var)

    def exit_calc(self):
        print('Bye!')
        quit()

    def help_calc(self):
        print('''
        The program calculates the sum of numbers
        and get substraction of number
        like then:
        1 + 1 + 2 - 1
        125 - 60
        must be space beetwine numbers and math operators
        Program can use variables in operions
                ''')


if __name__ == '__main__':
    calc = SmartCalculator()
