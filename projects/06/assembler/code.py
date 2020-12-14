class Code(object):
    """
    lalala
    """

    def __init__(self):
        self.dest_mnemonic = {
            '': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111'
        }

        self.comp_mnemonic = {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            'M': '1110000',
            '!D': '0001101',
            '!A': '0110001',
            '!M': '1110001',
            '-D': '0001111',
            '-A': '0110011',
            '-M': '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101'
        }

        self.jump_mnemonic = {
            '': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }

    
    def dest(self, mnemonic):
        try:
            return self.dest_mnemonic[mnemonic]
        except KeyError:
            print('Wrong mnemonic: {}!'.format(mnemonic))

    
    def comp(self, mnemonic):
        try:
            return self.comp_mnemonic[mnemonic]
        except KeyError:
            print('Wrong mnemonic: {}!'.format(mnemonic))


    def jump(self, mnemonic):
        try:
            return self.jump_mnemonic[mnemonic]
        except KeyError:
            print('Wrong mnemonic: {}!'.format(mnemonic))


def main():
    code = Code()

    print('Dest')
    print('\tAMD:', code.dest('AMD'))
    print('\tX:', code.dest('X'))

    print('Comp')
    print('\tD|M:', code.comp('D|M'))
    print('\tD/M:', code.comp('D/M'))

    print('Jump')
    print('\tJMP:', code.jump('JMP'))
    print('\tJUMP:', code.jump('JUMP'))


if __name__ == "__main__":
    main()