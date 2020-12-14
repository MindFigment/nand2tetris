from compilation_engine import CompilationEnginge

import click
from os import listdir
from os.path import isfile, join


@click.command()
@click.argument('input_file')
def main(input_file):
    """
    Runs jack analizer of input file, and creates xml output file.
    If input_file is a directory then compiles all jack files in there
    """

    ######################################
    ### Find all jack files to compile ###
    ######################################

    # If input_file is a directory
    if len(input_file.split('.')) == 1:
        if input_file[-1] == '/':
            input_file = input_file[:-1]
        input_files = [join(input_file, f) for f in listdir(input_file) if f.split('.')[1] == 'jack' and isfile(join(input_file, f))]
        output_files = [in_f.split('.')[0] + '_mine2.xml' for in_f in input_files]
        print('Input files: {}'.format(input_files))
    # If input_file is one specific jack file
    else:
        input_files = [input_file]  
        output_files = [input_file.split('.')[0] + '_mine2.xml']

    # Compile jack files one by one
    for input_file, output_file in zip(input_files, output_files):
        compilation_engine = CompilationEnginge(input_file, output_file)
        print('Analyzing: {}, saving into: {}'.format(input_file, output_file))
        compilation_engine.analyze()
        print('Analyzation completed!')
    print('ALL FILES ANALYZED!')



if __name__ == "__main__":
    main()