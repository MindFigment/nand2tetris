import click
import re
from iteration_utilities import deepflatten
import os


class JackTokenizer(object):
    """
    lalala
    """

    def __init__(self, input_file):


        ###################
        ### TOKEN TYPES ###
        ###################

        self.keyword_token = 'keyword'
        self.symbol_token = 'symbol'
        self.identifier_token = 'identifier'
        self.int_const = 'integerConstant'
        self.string_const = 'stringConstant'

        self.jack_symbols = [
            '{', '}',
            '(', ')',
            '[', ']',
            '-',
            '.',
            ',',
            ';',
            '+',
            '*',
            '/',
            '&',
            '|',
            '<', '>',
            '=',
            '~'
        ]

        #####################
        ### KEYWORD TYPES ###
        #####################

        # Used only when current token type is 'KEYWORD'

        self.key_class = 'class'
        self.key_method = 'method'
        self.key_function = 'function'
        self.key_constructor = 'constructor'
        self.key_int = 'int'
        self.key_boolean = 'boolean'
        self.key_char = 'char'
        self.key_void = 'void'
        self.key_if = 'if'
        self.key_var = 'var'
        self.key_static = 'static'
        self.key_field = 'field'
        self.key_let = 'let'
        self.key_do = 'do'
        self.key_if = 'if'
        self.key_else = 'else'
        self.key_while = 'while'
        self.key_return = 'return'
        self.key_true = 'true'
        self.key_false = 'false'
        self.key_null = 'null'
        self.key_this = 'this'

        self.jack_keywords = [
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'null',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return'
        ]

        self.token = None
        self.type = None
        # Keeping track whether we are inside multiline comment 
        # during reading input file
        self.inside_comment = False

        with open(input_file, 'r') as f:
            token_list = []
            for line in f:
                line = self._remove_whitespace(line)
                if line == '':
                    continue
                else:
                    tokenized_line = list(deepflatten(self._tokenize_line(line), ignore=str))
                    # print(50 * '*')
                    # print('LINE ======>', line)
                    # print('TOKENIZED =>', tokenized_line)
                    # print(50 * '*')
                    token_list += tokenized_line
            token_tuple = tuple(token_list)
            self.token_iter = iter(token_tuple)
            del token_tuple


    def advance(self):
        try:
            self.token = next(self.token_iter)
            return True
        except StopIteration:
            print('Tokenization is done')
            return False


    def token_type(self):
        if self.token in self.jack_keywords:
            self.type = self.keyword_token
            return self.type
        elif self.token in self.jack_symbols:
            self.type = self.symbol_token
            return self.type
        elif re.fullmatch(r'[a-zA-Z_][a-zA-z0-9_]*', self.token):
            self.type = self.identifier_token
            return self.type
        elif self.token.isdigit():
            self.type = self.int_const
            return self.type
        elif re.fullmatch(r'"[^"\n]*"', self.token):
            self.type = self.string_const
            return self.type
        else:
            raise ValueError('Ups! Something is wrong. Cannot classify token: "{}"'.format(self.token))


    def keyword(self):
        if self.token not in self.jack_keywords:
            raise ValueError('{} is not a jack keyword!'.format(self.token))
        elif self.token == self.key_class:
            return self.key_class
        elif self.token == self.key_method:
            return self.key_method
        elif self.token == self.key_function:
            return self.key_function
        elif self.token == self.key_constructor:
            return self.key_constructor
        elif self.token == self.key_int:
            return self.key_int
        elif self.token == self.key_boolean:
            return self.key_boolean
        elif self.token == self.key_char:
            return self.key_char
        elif self.token == self.key_void:
            return self.key_void
        elif self.token == self.key_var:
            return self.key_var
        elif self.token == self.key_static:
            return self.key_static
        elif self.token == self.key_field:
            return self.key_field
        elif self.token == self.key_let:
            return self.key_let
        elif self.token == self.key_do:
            return self.key_do
        elif self.token == self.key_if:
            return self.key_if
        elif self.token == self.key_else:
            return self.key_else
        elif self.token == self.key_while:
            return self.key_while
        elif self.token == self.key_return:
            return self.key_return
        elif self.token == self.key_true:
            return self.key_true
        elif self.token == self.key_false:
            return self.key_false
        elif self.token == self.key_null:
            return self.key_null
        elif self.token == self.key_this:
            return self.key_this
            
    
    def symbol(self):
        if self.token not in self.jack_symbols:
            raise ValueError('{} is not a jack symbol!'.format(self.token))
        else:
            if self.token == '<':
                return '&lt;'
            elif self.token == '>':
                return '&gt;'
            elif self.token == '"':
                return '&quot;'
            elif self.token == '&':
                return '&amp;'
            else:
                return self.token



    def identifier(self):
        if self.type == self.identifier_token:
            return self.token
        else:
            raise ValueError('{} is not an identifier!'.format(self.token))


    def int_val(self):
        if self.type == self.int_const:
            return int(self.token)
        else:
            raise ValueError('{} is not an integer!'.format(self.token))

    
    def string_val(self):
        if self.type == self.string_const:
            token = self.token[1:-1]
            return token
        else:
            raise ValueError('{} is not a string!'.format(self.token))
            

    def _remove_whitespace(self, line):
        line = line.strip()
        # Handling comments starting with // and between /** and */
        if line.startswith('//'):
            line = ''
        elif line.startswith('/**'):
            if not line.endswith('*/'):
                self.inside_comment = True
            line = ''
        elif line.endswith('*/'):
            self.inside_comment = False
            line = ''
        elif self.inside_comment == True:
            line = ''
        else:
            line = ' '.join(line.split())
            # Removing comments
            line = re.sub(r'\s+(//).*', '', line)
        return line


    def _tokenize_line(self, line):
        by_whitespace = re.split(r'''\s(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line)
        tokenized_line = []
        for mass in by_whitespace:
            tokenized_line += self._recursive_tokenize(mass)
        return tokenized_line


    def _recursive_tokenize(self, mass):
        # As first step split by .
        splited_by = None

        if '.' in mass:
            splited = re.split(r'''\.(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = '.'
        elif '(' in mass:
            splited = re.split(r'''\((?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = '('
        elif '[' in mass:
            splited = re.split(r'''\[(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = '['
        elif ')' in mass:
            splited = re.split(r'''\)(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = ')'
        elif ']' in mass:
            splited = re.split(r'''\](?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = ']'
        elif '-' in mass and mass != '-':
            splited = re.split(r'''\-(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = '-'
        elif '~' in mass and mass != '~':
            splited = re.split(r'''\~(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = '~'
        elif ';' in mass:
            splited = re.split(r'''\;(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = ';'
        elif ',' in mass:
            splited = re.split(r'''\,(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', mass)
            splited_by = ','
        else:
            # print('END OF RECURSION with {}'.format(mass))
            return [mass]

        splited_parts = []
        tokenized_mass = []
        # print('MASS:', mass)
        # print('SPLITED:', splited)
        for split in splited:
            # print('GOING DEEPER with {}'.format(split))
            splited_parts.append(self._recursive_tokenize(split))

        # print()
        # print()
        # print('SPLITED PARTS =======> {}'.format(splited_parts))
        # print()
        # print()

        tokenized_mass = self._assemble_splited_parts(splited_parts, splited_by)

        # Getting rid of ['']
        tokenized_mass = list(filter(lambda x: x != [''], tokenized_mass))

        # print()
        # print()
        # print('TOKENIZED MASS =======> {}'.format(tokenized_mass))
        # print()
        # print()

        return tokenized_mass


    def _assemble_splited_parts(self, splited, splited_by):
        tokenized_mass = []
        for i, token in enumerate(splited):
            if i == 0:
                tokenized_mass.append(token)
            else:
                tokenized_mass.append(splited_by)
                tokenized_mass.append(token)
        return tokenized_mass


@click.command()
@click.argument('input_file')
def main(input_file):
    output_filename = input_file.split('/')[-1].split('.')[0]
    directory = input_file.split('/')[:-1]
    output_file = os.path.join(*directory, output_filename + 'T_mine.xml')
    print('Output file: {}'.format(output_file))
    tokenizer = JackTokenizer(input_file)
    with open(output_file, 'w') as f:
        f.write('<tokens>\n')
        n = 0
        while tokenizer.advance():
            token_type = tokenizer.token_type()
            line_to_write = '<{0}> {1} </{0}>\n'.format(token_type, tokenizer.token)
            # print(str(n) + ':', line_to_write)
            f.write(line_to_write)
            n += 1
        f.write('</tokens>\n')


if __name__ == "__main__":
    main()