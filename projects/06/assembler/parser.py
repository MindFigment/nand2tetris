import click
import re


class Parser(object):
    """
    lalala
    """

    def __init__(self, input_file):

        self.a_command = 'A_COMMAND'
        self.c_command = 'C_COMMAND'
        self.l_command = 'L_COMMAND'

        self.first_pass = None
        self.second_pass = None
        self.is_first_pass_finished = False
        self.is_second_pass_finished = False
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
            self.first_pass = iter(command_tuple)
            self.second_pass = iter(command_tuple)
            del command_tuple


    def advance(self):
        try:
            if self.is_first_pass_finished == False:
                self.command = next(self.first_pass)
            else:
                self.command = next(self.second_pass)
            return True
        except StopIteration:
            if self.is_first_pass_finished == False:
                self.is_first_pass_finished = True
            else:
                self.is_second_pass_finished = True
            return False


    def command_type(self):
        if self.command.startswith('@'):
            return self.a_command
        elif re.match(r'\(\S+\)', self.command):
            return self.l_command
        elif re.match(r'([a-zA-Z]+=)?([a-zA-z]+)?(;[a-zA-Z]+)?', self.command):
            return self.c_command
        else:
            raise ValueError('Ups! Something is wrong. Cannot classify command: "{}" into one of 3 known categories: A, C or L command.'.format(self.command))


    def symbol(self):
        command_type = self.command_type()
        if command_type == self.a_command:
            return self.command[1:]
        elif command_type == self.l_command:
            return self.command[1:-1]
        else:
            raise ValueError('Wrong command type: {}! It should be "A_COMMAND" or "L_COMMAND".'.format(self.command))

    
    def dest(self):
        command_type = self.command_type()
        if command_type == self.c_command:
            split = self.command.split('=')
            if len(split) != 1:
                return split[0]
            else:
                return ''
        else:
            raise ValueError('Wrong command type: {}!. It can be "C_COMMAND" only.'.format(command_type))


    def comp(self):
        command_type = self.command_type()
        if command_type == self.c_command:
            split_1 = self.command.split('=')
            if len(split_1) != 1:
                return split_1[1].split(';')[0]
            else:
                return split_1[0].split(';')[0]
        else:
            raise ValueError('Wrong command type: {}!. It can be "C_COMMAND" only.'.format(command_type))


    def jump(self):
        command_type = self.command_type()
        if command_type == self.c_command:
            split = self.command.split(';')
            if len(split) != 1:
                return split[1]
            else:
                return ''
        else:
            raise ValueError('Wrong command type: {}!. It can be "C_COMMAND" only.'.format(command_type))


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
        if com_type == parser.c_command:
            print('\tDest:', parser.dest())
            print('\tComp:', parser.comp())
            print('\tJump:', parser.jump())
        else:
            print('\tSymbol:', parser.symbol())
        n += 1
    


if __name__ == "__main__":
    main()