import click
import re


class CodeWriter(object):

    def __init__(self, output_file):
        self.hack_f = None
        self.filename = None
        # Write code to output_file.asm
        self.hack_f = open(''.join([output_file, '.asm']), 'w') 
        self.c_push = 'C_PUSH'
        self.c_pop = 'C_POP'
        self.eq_n = 0
        self.gt_n = 0
        self.lt_n = 0
        self.ret_count = 0
        self.function_stack = ['']
        

    def end_loop(self):
        end_loop = [
            '(END)',
            '\t@END',
            '\t0;JMP'
        ]
        for line in end_loop:
            self.hack_f.write(line + '\n')


    def set_filename(self, filename):   
        self.filename = filename.split('/')[-1].split('.')[0]
        print('SET FILENAME: {}'.format(self.filename))

    
    def write_init(self):
        lines_to_write = [
            '@256',
            'D=A',
            '@SP',
            'M=D // Set SP (RAM[0]) to 256'
        ]
        
        self._write_lines(lines_to_write)

        self.write_call('Sys.init', 0)


    def write_function(self, function_name, num_locals):
        self.function_stack.append(function_name)
        # print('AAAAAAAAAADDDDDDDDDDDDDDD func: {}'.format(self.function_stack))
        # Initialize local arguments of the function to zero
        lines_to_write = [
            '({}) // HANDLING FUNCTION'.format(function_name),
            '@SP',
            'D=M'
        ]
        
        if num_locals != 0:
            set_local_args = (int(num_locals) - 1) * [
                'A=D',
                'M=0',
                'D=D+1'
            ] + [
                'A=D',
                'M=0',
                '@SP',
                'M=D'
            ]
        else:
            set_local_args = []

        lines_to_write += set_local_args

        self._write_lines(lines_to_write)


    def write_return(self):
        # print('BBBBBBBEEEEEEEEEFFFFFFFOOOOOOOORE del: {}'.format(self.function_stack))
        del self.function_stack[-1]
        # print('AAAAAAAAAAAFFFFFFFFFTTTTTTTEEERRR del: {}'.format(self.function_stack))
        lines_to_write = [
            '@LCL',
            'D=M',
            '@R8 // FRAME temp var storing LCL address',
            'M=D',
            '@5',
            'A=D-A // LCL - 5',
            'D=M',
            '@R9',
            'M=D // Return address *(FRAME - 5)',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@ARG',
            'A=M',
            'M=D // *ARG = pop()',
            '@ARG',
            'D=M',
            '@SP',
            'M=D+1 // Restore SP of the caller',
            '@R8',
            'M=M-1 // FRAME - 1',
            'A=M',
            'D=M',
            '@THAT',
            'M=D // Restore THAT of the caller *(FRAME - 1)',
            '@R8',
            'M=M-1 // FRAME - 2',
            'A=M',
            'D=M',
            '@THIS',
            'M=D // Restore THIS of the caller *(FRAME - 2)',
            '@R8',
            'M=M-1 // FRAME - 3',
            'A=M',
            'D=M',
            '@ARG',
            'M=D // Restore THIS of the caller *(FRAME - 3)',
            '@R8',
            'M=M-1 // FRAME - 4',
            'A=M',
            'D=M',
            '@LCL',
            'M=D // Restore THIS of the caller *(FRAME - 4)',
            '@R9',
            'A=M',
            '0;JMP // Goto return-address (in the callers code)'
        ]

        self._write_lines(lines_to_write)

    
    def write_call(self, function_name, num_args):
        reposition_arg_by = int(num_args) + 5
        return_address = 'return_address-{}'.format(self.ret_count)
        self.ret_count += 1
        lines_to_write = [
            '@{}'.format(return_address),
            'D=A',
            '@SP',
            'A=M',
            'M=D // save return-address on the stack',
            '@SP',
            'M=M+1 // update the stack',
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D // save LCL of the calling function',
            '@SP',
            'M=M+1',
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D // save ARG of the calling function',
            '@SP',
            'M=M+1',
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D // save THIS of the calling function',
            '@SP',
            'M=M+1',
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D // save THAT of the calling function',
            '@SP',
            'M=M+1',
            '@{}'.format(reposition_arg_by),
            'D=A',
            '@SP',
            'D=M-D',
            '@ARG',
            'M=D // Reposition ARG (SP-num_args-5)',
            '@SP',
            'D=M',
            '@LCL',
            'M=D // Reposition LCL (LCL = SP)',
            '@{}'.format(function_name),
            '0;JMP // Transfer control (goto f)',
            '({}) // Declare label for the return-address'.format(return_address)
        ]

        self._write_lines(lines_to_write)


    def write_if(self, label):
        if self.function_stack[-1] == '':
            final_label = label
        else:
            final_label = '{}${}'.format(self.function_stack[-1], label)
        
        lines_to_write = [
            '@SP // START: if-goto',
            'M=M-1',
            'A=M',
            'D=M // Check if there is true value on top of the stack',
            '@{}'.format(final_label),
            'D;JNE // END: if-goto'
        ]

        self._write_lines(lines_to_write)


    def write_goto(self, label):
        if self.function_stack[-1] == '':
            final_label = label
        else:
            final_label = '{}${}'.format(self.function_stack[-1], label)
        
        lines_to_write = [
            '@{}'.format(final_label),
            '0;JMP'
        ]

        self._write_lines(lines_to_write)

    
    def write_label(self, label):
        if self.function_stack[-1] == '':
            final_label = label
        else:
            final_label = '{}${}'.format(self.function_stack[-1], label)

        lines_to_write = [
            '({})'.format(final_label)
        ]

        self._write_lines(lines_to_write)


    def write_arithmetic(self, command):
        lines_to_write = []
        if command == 'add':
            lines_to_write = [
                '@SP', 
                'A=M-1',
                'D=M', 
                'A=A-1', 
                'M=M+D', 
                '@SP', 
                'M=M-1'
            ]

        elif command == 'sub':
            lines_to_write = [
                '@SP', 
                'A=M-1',
                'D=M', 
                'A=A-1', 
                'M=M-D', 
                '@SP', 
                'M=M-1'
            ]

        elif command == 'neg':
            lines_to_write = [
                '@SP',
                'A=M-1',
                'M=-M'
            ]

        elif command == 'eq':
            lines_to_write = [
                '@SP', 
                'A=M-1', 
                'D=M', 
                'A=A-1',
                'D=D-M',
                '@ZERO_' + str(self.eq_n), 
                'D;JEQ', 
                '@R0', 
                'D=A',
                '@ONE_' + str(self.eq_n),
                '0;JMP',
                '(ZERO_' + str(self.eq_n) + ')',
                '@R1',
                'D=A',
                'D=-D',
                '(ONE_' + str(self.eq_n) + ')',
                '@SP', 
                'M=M-1',
                'A=M-1',
                'M=D'
            ]
            self.eq_n += 1

        elif command == 'gt':
            lines_to_write = [
                '@SP', 
                'A=M-1', 
                'D=M', 
                'A=A-1', 
                'D=M-D',
                '@GT_' + str(self.gt_n), 
                'D;JGT', 
                '@R0', 
                'D=A',
                '@NOTGT_' + str(self.gt_n),
                '0;JMP',
                '(GT_' + str(self.gt_n) + ')',
                '@R1',
                'D=A',
                'D=-D',
                '(NOTGT_' + str(self.gt_n) + ')',
                '@SP', 
                'M=M-1',
                'A=M-1',
                'M=D'
            ]
            self.gt_n += 1

        elif command == 'lt':
            lines_to_write = [
                '@SP', 
                'A=M-1', 
                'D=M', 
                'A=A-1',
                'D=M-D',
                '@LT_' + str(self.lt_n), 
                'D;JLT', 
                '@R0', 
                'D=A',
                '@NOTLT_' + str(self.lt_n),
                '0;JMP',
                '(LT_' + str(self.lt_n) + ')',
                '@R1',
                'D=A',
                'D=-D',
                '(NOTLT_' + str(self.lt_n) + ')',
                '@SP', 
                'M=M-1',
                'A=M-1',
                'M=D'
            ]
            self.lt_n += 1

        elif command == 'and':
            lines_to_write = [
                '@R2',
                'D=A',
                '@SP', 
                'A=M-1', 
                'D=M-D', 
                'A=A-1',
                'D=D&M',
                '@SP', 
                'M=M-1',
                'A=M-1',
                'M=D'
            ]

        elif command == 'or':
            lines_to_write = [
                '@SP', 
                'A=M-1', 
                'D=M', 
                'A=A-1',
                'D=D|M',
                '@SP', 
                'M=M-1',
                'A=M-1',
                'M=D'
            ]

        elif command == 'not':
            # VM represents true as -1 and false as 0
            # So -1 + 1 = 0, then negate to get still 0
            # And 0 + 1 = 1, then negate to get -1
            lines_to_write = [
                '@SP', 
                'A=M-1', 
                'M=!M'
            ]

        self._write_lines(lines_to_write)


    def write_push_pop(self, push_or_pop, segment, index):
        lines_to_write = []

        #####################
        ### PUSH COMMANDS ###
        #####################

        if push_or_pop == self.c_push:
            if segment == 'constant':
                lines_to_write = [
                    ''.join(['@', str(index)]),
                    'D=A',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ]

            elif segment == 'local':
                lines_to_write = self._push_l_a_t_t('LCL', index)

            elif segment == 'argument':
                lines_to_write = self._push_l_a_t_t('ARG', index)

            elif segment == 'this':
                lines_to_write = self._push_l_a_t_t('THIS', index)

            elif segment == 'that':
                lines_to_write = self._push_l_a_t_t('THAT', index)

            elif segment == 'temp':
                lines_to_write = [
                    ''.join(['@R', str(index)]),
                    'D=A',
                    '@R5',
                    'A=A+D',
                    'D=M',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ]

            elif segment == 'pointer':
                if index == 0:
                    this_or_that = 'THIS'
                else:
                    this_or_that = 'THAT'
                lines_to_write = [
                    '@{}'.format(this_or_that),
                    'D=M',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ]

            elif segment == 'static':
                lines_to_write = [
                    '@{}.{}'.format(self.filename, index),
                    'D=M',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ]

        ####################
        ### POP COMMANDS ###
        ####################

        elif push_or_pop == self.c_pop:
            if segment == 'constant':
                raise ValueError('Cannot pop constant i!')

            elif segment == 'local':
                lines_to_write = self._pop_l_a_t_t('LCL', index)

            elif segment == 'argument':
                lines_to_write = self._pop_l_a_t_t('ARG', index)

            elif segment == 'this':
                lines_to_write = self._pop_l_a_t_t('THIS', index)

            elif segment == 'that':
                lines_to_write = self._pop_l_a_t_t('THAT', index)

            elif segment == 'temp':
                lines_to_write = [
                    ''.join(['@R', str(index)]),
                    'D=A',
                    '@R5',
                    'A=A+D',
                    'D=A',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M-1',
                    '@SP',
                    'A=M',
                    'D=M',
                    '@SP',
                    'A=M+1',
                    'A=M',
                    'M=D'
                ]

            elif segment == 'pointer':
                if index == 0:
                    this_or_that = 'THIS'
                else:
                    this_or_that = 'THAT'
                lines_to_write = [
                    '@SP',
                    'M=M-1',
                    'A=M',
                    'D=M',
                    '@{}'.format(this_or_that),
                    'M=D'
                ]

            elif segment == 'static':
                lines_to_write = [
                    '@SP',
                    'M=M-1',
                    'A=M',
                    'D=M',
                    '@{}.{}'.format(self.filename, index),
                    'M=D'
                ]

        self._write_lines(lines_to_write)


    def close(self):
        if self.hack_f:
            self.end_loop()
            self.hack_f.close()
            self.hack_f = None


    def _push_l_a_t_t(self, segment_symbol, index):
        lines_to_write = [
            ''.join(['@R', str(index)]),
            'D=A',
            '@{}'.format(segment_symbol),
            'A=M+D',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]
        return lines_to_write

    
    def _pop_l_a_t_t(self, segment_symbol, index):
        lines_to_write = [
            ''.join(['@R', str(index)]),
            'D=A',
            '@{}'.format(segment_symbol),
            'A=M+D',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M-1',
            '@SP',
            'A=M',
            'D=M',
            '@SP',
            'A=M+1',
            'A=M',
            'M=D'
        ]
        return lines_to_write

    
    def _write_lines(self, lines_to_write):
        print(50 * '*')
        for line in lines_to_write:
            if re.match(r'\(\S+\)', line):
                self.hack_f.write(line + '\n')
                print('\t' + line)
            else:
                self.hack_f.write('\t' + line + '\n')
                print('\t\t' + line)
        print(50 * '*')


@click.command()
@click.argument('output_file')
def main(output_file):
    # program = [
    #     'push constant 7',
    #     'push constant 8',
    #     'add'
    # ]
    code_writer = CodeWriter(output_file)
    code_writer.write_push_pop('push', 'constant', 7)
    code_writer.write_push_pop('push', 'constant', 8)
    code_writer.write_arithmetic('add')
    code_writer.close()
    


if __name__ == "__main__":
    main()