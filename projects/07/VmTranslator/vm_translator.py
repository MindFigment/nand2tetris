from code_writer import CodeWriter
from parser import Parser

import click
from os import listdir
from os.path import isfile, join


@click.command()
@click.argument('input_file')
def main(input_file):
    if len(input_file.split('.')) == 1:
        if input_file[-1] == '/':
            input_file = input_file[:-1]
        output_file = join(input_file, input_file.split('/')[-1])
        input_files = [join(input_file, f) for f in listdir(input_file) if f.split('.')[1] == 'vm' and f != 'Sys.vm' and isfile(join(input_file, f))]
        input_files.insert(0, join(input_file, 'Sys.vm'))
        print('Input files: {}'.format(input_files))
    else:
        input_files = [input_file]  
        directory = '/'.join(input_file.split('/')[:-1])
        output_file = join(directory, input_file.split('/')[-1].split('.')[0])

    code_writer = CodeWriter(output_file)
    code_writer.write_init()

    for input_file in input_files:
        parser = Parser(input_file)
        code_writer.set_filename(input_file)
        n = 0
        while parser.advance():
            com_type = parser.command_type()
            print('LINE {}'.format(n))
            print('\tcom type: {}'.format(com_type))
            print('\tcommand: {}'.format(parser.command))
            if com_type != parser.c_return:
                arg1 = parser.arg1()   
                if com_type in [parser.c_push, parser.c_pop, parser.c_function, parser.c_call]:
                    arg2 = parser.arg2()
                    
            if com_type == parser.c_arithmetic:
                code_writer.write_arithmetic(arg1)
            elif com_type in [parser.c_pop, parser.c_push]:
                code_writer.write_push_pop(com_type, arg1, int(arg2))
            elif com_type == parser.c_label:
                code_writer.write_label(arg1)
            elif com_type == parser.c_goto:
                code_writer.write_goto(arg1)
            elif com_type == parser.c_if:
                code_writer.write_if(arg1)
            elif com_type == parser.c_function:
                code_writer.write_function(arg1, arg2)
            elif com_type == parser.c_return:
                code_writer.write_return()
            elif com_type == parser.c_call:
                code_writer.write_call(arg1, arg2)
            n += 1
    code_writer.close()



if __name__ == "__main__":
    main()


    
