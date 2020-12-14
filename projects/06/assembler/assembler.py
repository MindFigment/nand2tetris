import click

from parser import Parser
from code import Code
from symbol_table import SymbolTable


class Assembler(object):
    """
    lalala
    """

    def __init__(self, asm_file):
        self.asm_file = asm_file
        self.hack_file = ''.join([asm_file.split('.')[0], '.hack'])
        self.parser = Parser(asm_file)
        self.code = Code()
        self.symbol_table = SymbolTable()


    def assembly(self):
        print('Starting to assembly {} file...'.format(self.asm_file))
        with open(self.hack_file, 'w') as hack_f:

            ##################
            ### First pass ###
            ##################

            line_number = 0
            while self.parser.advance():
                command_type = self.parser.command_type()
                if command_type == self.parser.c_command or command_type == self.parser.a_command:
                    line_number += 1

                elif command_type == self.parser.l_command:
                    symbol = self.parser.symbol()
                    self.symbol_table.add_entry(symbol, line_number)

                else:
                    raise ValueError('Ups!')

            ###################
            ### Second pass ###
            ###################

            next_var_address = 16
            while self.parser.advance():
                command_type = self.parser.command_type()
                if command_type == self.parser.c_command:
                    dest_bin = self.code.dest_mnemonic[self.parser.dest()]
                    comp_bin = self.code.comp_mnemonic[self.parser.comp()]
                    jump_bin = self.code.jump_mnemonic[self.parser.jump()]
                    word_16 = ''.join(['111', comp_bin, dest_bin, jump_bin, '\n'])

                elif command_type == self.parser.a_command:
                    symbol = self.parser.symbol()
                    if symbol.isdigit():
                        address_bin = format(int(symbol), 'b').zfill(15)
                    else:
                        if self.symbol_table.contains(symbol) == False:
                            self.symbol_table.add_entry(symbol, next_var_address)
                            next_var_address += 1    

                        address_int = self.symbol_table.get_address(symbol)
                        address_bin = format(address_int, 'b').zfill(15)
                    word_16 = ''.join(['0', address_bin, '\n'])

                elif command_type == self.parser.l_command:
                    continue
                else:
                    raise ValueError('Ups!')
                hack_f.write(word_16)
        print('Successfully finished the assembly process :)')


@click.command()
@click.argument('asm_file')
def main(asm_file):
    assembler = Assembler(asm_file)
    assembler.assembly()
    


if __name__ == "__main__":
    main()