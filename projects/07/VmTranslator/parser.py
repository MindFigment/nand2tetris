import click
import re


class Parser(object):
    """
    lalala
    """

    def __init__(self, input_file):


        #####################
        ### COMMAND TYPES ###
        #####################

        self.c_arithmetic = 'C_ARITHMETIC'
        self.c_push = 'C_PUSH'
        self.c_pop = 'C_POP'
        self.c_label = 'C_LABEL'
        self.c_goto = 'C_GOTO'
        self.c_if = 'C_IF'
        self.c_function = 'C_FUNCTION'
        self.c_return = 'C_RETURN'
        self.c_call = 'C_CALL'

        self.al_commands = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

        self.command = None

        with open(input_file, 'r') as f:
            command_list = []
            for command in f:
                command = self._remove_whitespace(command)
                if command == '':
                    continue
                else:
                    command_list.append(command)
            command_tuple = tuple(command_list)
            self.command_iter = iter(command_tuple)
            del command_tuple


    def advance(self):
        try:
            self.command = next(self.command_iter)
            return True
        except StopIteration:
            return False


    def command_type(self):
        if self.command in self.al_commands:
            return self.c_arithmetic
        elif self.command.startswith('push'):
            return self.c_push
        elif self.command.startswith('pop'):
            return self.c_pop
        elif self.command.startswith('goto'):
            return self.c_goto
        elif self.command.startswith('if-goto'):
            return self.c_if
        elif self.command.startswith('label'):
            return self.c_label
        elif self.command.startswith('function'):
            return self.c_function
        elif self.command.startswith('call'):
            return self.c_call
        elif self.command.startswith('return'):
            return self.c_return
        else:
            raise ValueError('Ups! Something is wrong. Cannot classify command: "{}" into one of 7 known categories: push, pop, if-goto, label, funciton, call, return commands.'.format(self.command))


    def arg1(self):
        if self.command_type() == self.c_return:
            raise ValueError('Wrong command type: {}! It cannot be "C_RETURN" command.'.format(self.command))
        elif self.command_type() == self.c_arithmetic:
            return self.command
        else:
            return self.command.split(' ')[1]


    def arg2(self):
        avaiable_commands = [self.c_push, self.c_pop, self.c_function, self.c_call]
        if self.command_type() not in avaiable_commands:
            raise ValueError('Wrong command type: {}! It cannot be any of this commands: {}.'.format(self.command, avaiable_commands))
        else:
            return self.command.split(' ')[2]

    
    def _remove_whitespace(self, command):
        command = command.strip()
        if command.startswith('//'):
            command = ''
        else:
            command = ' '.join(command.split())
            command = re.sub(r'\s+(//).*', '', command)
        return command


@click.command()
@click.argument('input_file')
def main(input_file):
    parser = Parser(input_file)
    n = 0
    while parser.advance():
        com_type = parser.command_type()
        print('Line {}:'.format(n))
        print('\tCommand:', parser.command)
        print('\tType:', com_type)
        if com_type != parser.c_return:
            print('\tArg1:', parser.arg1())
        if com_type in [parser.c_push, parser.c_pop, parser.c_function, parser.c_call]:
            print('\tArg2:', parser.arg2())
        n += 1
    


if __name__ == "__main__":
    main()