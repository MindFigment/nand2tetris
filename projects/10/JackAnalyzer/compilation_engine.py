from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable
from vm_writer import VMWriter

import re 


class CompilationEnginge(object):
    """
    lalala
    """

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.out = open(output_file, 'w')
        self.token = None
        self.class_name = None

        #######################
        ### PROJECT 11 CODE ###
        #######################

        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)

        #######################


    def analyze(self):
        self.token = self.tokenizer.advance()
        self.compile_class()
        self.close()
        print('CLASS TABLE:')
        print(self.symbol_table.class_table)


    def close(self):
        if self.out:
            self.out.close()
            self.out = None


    def advance(self):
        self.token = self.tokenizer.advance()


    def write_to_out(self):
        pass


    def format_line(self, defined_or_used=''):
        token_type = self.tokenizer.token_type()
        running_index = ''
        if token_type == self.tokenizer.keyword_token:
            meat = self.tokenizer.keyword()
            defined_or_used=''
        elif token_type == self.tokenizer.symbol_token:
            meat = self.tokenizer.symbol()
            defined_or_used=''
        elif token_type == self.tokenizer.identifier_token:
            meat = self.tokenizer.identifier()

            #######################
            ### PROJECT 11 CODE ###
            #######################

            # Extending compilaiton engine to output <var/argument/static/field...> instead of <indentifier>
            name = self.tokenizer.token
            if self.symbol_table.kind_of(name):
                token_type = self.symbol_table.kind_of(name)
                running_index = str(self.symbol_table.index_of(name))
            elif name[0].islower():
                token_type = 'subroutine'
            else:
                token_type = 'class'

            #######################  

        elif token_type == self.tokenizer.int_const:
            meat = self.tokenizer.int_val()
            defined_or_used=''
        elif token_type == self.tokenizer.string_const:
            meat = self.tokenizer.string_val()
            defined_or_used=''
        else:
            raise ValueError('Something went wrong with token: {}'.format(self.token))
        
        if defined_or_used != '':
            defined_or_used += ' '
        if running_index != '':
            running_index = ' ' + running_index
        formated_line = '<{2}{0}{3}> {1} </{2}{0}{3}>\n'.format(token_type, meat, defined_or_used, running_index)
        return formated_line


    #########################
    ### PROGARM STRUCTURE ###
    #########################

    def compile_class(self):
        """
        ####################################################################
        ### class: 'class' className '{' classVarDec* subroutineDec* '}' ###
        ####################################################################
        """

        self.out.write('<class>\n')

        # 'class'
        keyword_line = self.format_line()
        self.out.write(keyword_line)
        
        # className
        self.advance()

        #######################
        ### PROJECT 11 CODE ###
        #######################

        self.class_name = self.tokenizer.token

        ####################### 

        identifier_line = self.format_line('defined')
        self.out.write(identifier_line)

        # '{'
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        ### classVarDec* subroutineDec* ###
        self.advance()
        # classVarDec*
        while self.tokenizer.token_type() == self.tokenizer.keyword_token and self.tokenizer.keyword() in [self.tokenizer.key_field, self.tokenizer.key_static]:
            self.compile_class_var_dec()
        
        # subroutineDec*
        while  self.tokenizer.token_type() == self.tokenizer.keyword_token and self.tokenizer.keyword() in [self.tokenizer.key_function, self.tokenizer.key_method, self.tokenizer.key_constructor]:
            self.compile_subroutine()

        # '}'
        if  self.tokenizer.token_type() == self.tokenizer.symbol_token:
            # Class compilation is done
            symbol_line = self.format_line()
            self.out.write(symbol_line)
        else:
            raise ValueError('Something went wrong')

        # Closing with </class>
        self.out.write('</class>\n')
        is_sucessfull = not(self.advance())
        if is_sucessfull:
            print('Compilation enginge succesfully finished')
        else:
            print('Something went wrong!')


    def compile_class_var_dec(self):
        """
        #######################################################################
        ### classVarDec: ('static'|'field') type varName (',' varName)* ';' ###
        #######################################################################
        """

        self.out.write('<classVarDec>\n')

        #######################
        ### PROJECT 11 CODE ###
        #######################

        # Extract field or static
        # field_or_static = re.match('<[a-z]*>', field_or_static_line)[0][1:-1]
        field_or_static = self.tokenizer.token

        #######################

        #  ('static' | 'field')
        field_or_static_line = self.format_line()
        self.out.write(field_or_static_line)

        # type
        self.advance()

        #######################
        ### PROJECT 11 CODE ###
        #######################

        # Extract token type
        type_ = self.tokenizer.token

        #######################

        type_line = self.format_line()
        self.out.write(type_line)

        # varName
        self.advance()

        #######################
        ### PROJECT 11 CODE ###
        #######################

        self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind=field_or_static)

        #######################

        varname_line = self.format_line('defined')
        self.out.write(varname_line)

        # (',' varName)*
        self.advance()
        symbol = self.tokenizer.symbol()
        while symbol == ',':
            colon_line = self.format_line()
            self.out.write(colon_line)
            self.advance()

            #######################
            ### PROJECT 11 CODE ###
            #######################

            self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind=field_or_static)

            #######################

            varname_line = self.format_line('defined')
            self.out.write(varname_line)
            self.advance()
            symbol = self.tokenizer.symbol()
        # symbol == ';'
        semicolon_line = self.format_line()
        self.out.write(semicolon_line)
        self.advance()

        self.out.write('</classVarDec>\n')


    def compile_subroutine(self):
        """
        ###########################################################################
        ### subroutineDec: ('constructor'|'function'|'method')                  ###             
        ###                ('void' | type) subroutineName '(' parameterList ')' ###
        ###                subroutineBody                                       ###
        ###########################################################################
        """

        #######################
        ### PROJECT 11 CODE ###
        #######################

        print()
        print('SUBROUTINE TABLE:')
        print(self.symbol_table.subroutine_table)
        print()
        self.symbol_table.start_subroutine()
        self.symbol_table.define(name='this', type_=self.class_name, kind='argument')

        #######################

        self.out.write('<subroutineDec>\n')

        # ('constructor'|'function'|'method')
        constructor_function_method_line = self.format_line()
        self.out.write(constructor_function_method_line)

        # ('void' | type)
        self.advance()
        void_or_type_line = self.format_line()
        self.out.write(void_or_type_line)

        # subroutineName 
        self.advance()
        subroutine_name_line = self.format_line('defined')
        self.out.write(subroutine_name_line)

        # '(' 
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # parameterList
        self.advance()
        self.compile_parameter_list()

        # ')' 
        symbol_line = self.format_line()
        self.out.write(symbol_line)
        
        ##################################################
        ### subroutineBody: '{' varDec* statements '}' ###
        ##################################################
        
        self.out.write('<subroutineBody>\n')

        # '{'
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        ###############
        ### varDec* ###
        ###############

        self.advance()
        while self.tokenizer.token == self.tokenizer.key_var:
            self.compile_var_dec()

        ##################
        ### statements ###
        ##################

        self.compile_statements()
        
        # '}'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()

        self.out.write('</subroutineBody>\n')
        self.out.write('</subroutineDec>\n')

        #######################
        ### PROJECT 11 CODE ###
        #######################

        print()
        print('SUBROUTINE TABLE:')
        print(self.symbol_table.subroutine_table)
        print()

        #######################


    def compile_parameter_list(self):
        """
        ############################################################
        ### parameterList: ((type varName) (',' type varName)*)? ###
        ############################################################
        """

        self.out.write('<parameterList>\n')

        # If token type is symbol then we have empty parameter list
        # If we have symbol token then it means our parameter list is fully processed
        if self.tokenizer.token_type() != self.tokenizer.symbol_token:
            
            # type

            #######################
            ### PROJECT 11 CODE ###
            #######################

            type_ = self.tokenizer.token

            #######################

            type_line = self.format_line()
            self.out.write(type_line)
            
            # varName
            self.advance()

            #######################
            ### PROJECT 11 CODE ###
            #######################

            self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind='argument')

            #######################

            var_name_line = self.format_line('defined')
            self.out.write(var_name_line)

            # If next token is ',' we have more then one parameter
            self.advance()
            while self.tokenizer.token_type() == self.tokenizer.symbol_token and self.tokenizer.symbol() == ',':
                # ','
                comma_line = self.format_line()
                self.out.write(comma_line)

                # type
                self.advance()

                #######################
                ### PROJECT 11 CODE ###
                #######################

                type_ = self.tokenizer.token

                #######################

                type_line = self.format_line()
                self.out.write(type_line)

                # varName
                self.advance()

                #######################
                ### PROJECT 11 CODE ###
                #######################

                self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind='argument')

                # We are in new subroutine so add next nested scope
                # self.symbol_table.start_subroutine()

                #######################

                var_name_line = self.format_line('defined')
                self.out.write(var_name_line)

                self.advance()

        self.out.write('</parameterList>\n')



    def compile_var_dec(self):
        """
        #####################################################
        ### varDec: 'var' type varName (',' varName)* ';' ###
        #####################################################
        """

        self.out.write('<varDec>\n')

        # var
        var_line = self.format_line()
        self.out.write(var_line)

        # type
        self.advance()

        #######################
        ### PROJECT 11 CODE ###
        #######################

        type_ = self.tokenizer.token

        #######################

        type_line = self.format_line()
        self.out.write(type_line)

        # varName
        self.advance()

        #######################
        ### PROJECT 11 CODE ###
        #######################

        self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind='local')

        #######################

        var_name_line = self.format_line('defined')
        self.out.write(var_name_line)

        # (',' varName)*
        self.advance()
        while self.tokenizer.symbol() == ',':
            # ','
            comma_line = self.format_line()
            self.out.write(comma_line)

            # varName
            self.advance()

            #######################
            ### PROJECT 11 CODE ###
            #######################

            self.symbol_table.define(name=self.tokenizer.token, type_=type_, kind='local')

            #######################

            var_name_line = self.format_line('defined')
            self.out.write(var_name_line)

            self.advance()

        # ';'
        semicolon_line = self.format_line()
        self.out.write(semicolon_line)

        self.advance()

        self.out.write('</varDec>\n')


    ##################
    ### STATEMENTS ###
    ##################

    def compile_statements(self):
        """
        ##############################
        ### statements: statement* ###
        ##############################
        """
        
        self.out.write('<statements>\n')

        while self.tokenizer.token_type() != self.tokenizer.symbol_token:
            
            keyword = self.tokenizer.keyword()
            # letStatement
            if keyword == self.tokenizer.key_let:
                self.compile_let()

            # ifStatement
            elif keyword == self.tokenizer.key_if:
                self.compile_if()

            # whileStatement
            elif keyword == self.tokenizer.key_while:
                self.compile_while()

            # doStatement
            elif keyword == self.tokenizer.key_do:
                self.compile_do()

            # returnStatement
            elif keyword == self.tokenizer.key_return:
                self.compile_return()

            else:
                raise ValueError('Wrong statement: {}'.format(keyword))

        self.out.write('</statements>\n')


    def compile_do(self):
        """
        ############################################
        ### doStatement: 'do' subroutineCall ';' ###
        ############################################
        """

        self.out.write('<doStatement>\n')

        # 'do'
        do_line = self.format_line()
        self.out.write(do_line)

        # subroutineCall
        self.advance()
        self.compile_subroutine_call()

        # ';'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()

        self.out.write('</doStatement>\n')


    def compile_let(self):
        """
        ############################################################################
        ### letStatement: 'let' varName ('[' expression ']')? '=' expression ';' ###
        ############################################################################
        """

        self.out.write('<letStatement>\n')

        # let 
        let_line = self.format_line()
        self.out.write(let_line)

        # varName
        self.advance()

        var_name_line = self.format_line('used')
        self.out.write(var_name_line)

        # Check if '[' or '='
        self.advance()
        if self.tokenizer.token == '[':
            # '['
            symbol_line = self.format_line()
            self.out.write(symbol_line)

            # expression
            self.advance()
            self.compile_expression()

            # ']'
            symbol_line = self.format_line()
            self.out.write(symbol_line)
            self.advance()

        # '='
        symbol_line = self.format_line()
        self.out.write(symbol_line)
        
        # expression
        self.advance()
        self.compile_expression()

        # ';'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()

        self.out.write('</letStatement>\n')


    def compile_while(self):
        """
        #####################################################################
        ### whileStatement: 'while' '(' expression ')' '{' statements '}' ###
        #####################################################################
        """

        self.out.write('<whileStatement>\n')

        # 'while'
        while_line = self.format_line()
        self.out.write(while_line)

        # '('
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # expression
        self.advance()
        self.compile_expression()

        # ')'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # '{'
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # statements
        self.advance()
        self.compile_statements()

        # '}'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()

        self.out.write('</whileStatement>\n')


    def compile_return(self):
        """
        ################################################
        ### ReturnStatement 'return' expression? ';' ###
        ################################################
        """

        self.out.write('<returnStatement>\n')

        # 'return'
        return_line = self.format_line()
        self.out.write(return_line)

        # Ceck if expression
        self.advance()
        if self.tokenizer.token != ';':
            # 'expression'
            self.compile_expression()

        # ';'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()

        self.out.write('</returnStatement>\n')


    def compile_if(self):
        """
        ###############################################################
        ### ifStatement: 'if' '(' expression ')' '{' statements '}' ###
        ###              ('else' '{' statements '}')?               ###
        ###############################################################
        """

        self.out.write('<ifStatement>\n')

        # 'if'
        if_line = self.format_line()
        self.out.write(if_line)

        # '('
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # expression
        self.advance()
        self.compile_expression()

        # ')'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # '{'
        self.advance()
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # statements
        self.advance()
        self.compile_statements()

        # '}'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # Check if there is 'else' part of ifStatement
        self.advance()
        if self.tokenizer.token_type() == self.tokenizer.keyword_token and self.tokenizer.keyword() == 'else':
            # 'else'
            else_line = self.format_line()
            self.out.write(else_line)

            # '{'
            self.advance()
            symbol_line = self.format_line()
            self.out.write(symbol_line)

            # statements
            self.advance()
            self.compile_statements()

            # '}'
            symbol_line = self.format_line()
            self.out.write(symbol_line)

            self.advance()

        self.out.write('</ifStatement>\n')

    ###################
    ### EXPRESSIONS ###
    ###################

    def compile_subroutine_call(self, skip_subroutine_name=False):
        """
        ############################################################################
        ### subroutineCall: subroutineName '(' expressionList ')' | (className | ###
        ### varName) '.' subroutineName '(' expressionList ')'                   ###
        ############################################################################
        """

        if not skip_subroutine_name:
            # subroutineName or className or varName
            subroutine_class_var_name_line = self.format_line('used')
            self.out.write(subroutine_class_var_name_line)
            self.advance()

        # Check '(' or '.'
        if self.tokenizer.token == '.':
            # '.'
            symbol_line = self.format_line()
            self.out.write(symbol_line)
            
            # subroutineName
            self.advance()
            subroutine_name_line = self.format_line('used')
            self.out.write(subroutine_name_line)

            self.advance()

        # '('
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        # expressionList
        self.advance()
        self.compile_expression_list()

        # ')'
        symbol_line = self.format_line()
        self.out.write(symbol_line)

        self.advance()


    def compile_expression(self):
        """
        ###################################
        ### expression: term (op term)* ###
        ###################################
        """

        self.out.write('<expression>\n')

        ops = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

        # 'term'
        self.compile_term()

        # Check if there is (op term)* part
        while self.tokenizer.token in ops:
            # op
            op_line = self.format_line()
            self.out.write(op_line)

            # term
            self.advance()
            self.compile_term()

        self.out.write('</expression>\n')

    
    def compile_term(self):
        """
        ################################################################
        ###  integerConstant | stringConstant | keywordConstant |    ###
        ###  varName | varName '[' expression ']' | subroutineCall | ###
        ###  '(' expression ')' | unaryOp term                       ###
        ################################################################
        """

        self.out.write('<term>\n')

        unary_ops = ['-', '~']

        #############################################
        ### constant, name, expression or unaryOp ###
        #############################################

        # '(' expression ')'
        if self.tokenizer.token == '(':
            # '('
            symbol_line = self.format_line()
            self.out.write(symbol_line)

            # expression
            self.advance()
            self.compile_expression()

            # ')'
            symbol_line = self.format_line()
            self.out.write(symbol_line)

            self.advance()
        
        # unaryOp term
        elif self.tokenizer.token in unary_ops:
            # unaryOp
            unary_op_line = self.format_line()
            self.out.write(unary_op_line)

            # term
            self.advance()
            self.compile_term()

        # integerConstant | stringConstant | keywordConstant |
        # varName | varName '[' expression ']' | subroutineCall
        else:
            # constant or name
            constant_or_name = self.format_line('used')
            self.out.write(constant_or_name)

            # varName '[' expression ']' | subroutineCall or end of compile_term function
            # Check if expression: '[', subroutineCall: '(' with parameter skip_subroutine_name = True,
            # otherwise end of compile_term function
            self.advance()
            # '[' expression ']'
            if self.tokenizer.token == '[':
                # '['
                symbol_line = self.format_line()
                self.out.write(symbol_line)

                # expression
                self.advance()
                self.compile_expression()

                # ']'
                symbol_line = self.format_line()
                self.out.write(symbol_line)

                self.advance()
            
            # subroutineCall with skip_subroutine_name=True
            elif self.tokenizer.token in ['(', '.']:
                self.compile_subroutine_call(skip_subroutine_name=True)

        self.out.write('</term>\n')


    def compile_expression_list(self):
        """
        ########################################################
        ### expressionList: (expression (',' expression)* )? ###
        ########################################################
        """

        self.out.write('<expressionList>\n')

        # Check if token is ')', if so we got empty expression list
        if self.tokenizer.token != ')':
            # 'expression'
            self.compile_expression()

            # Check if token is ',', if so we got more expressions
            while self.tokenizer.token == ',':
                # ','
                comma_line = self.format_line()
                self.out.write(comma_line)

                # expression
                self.advance()
                self.compile_expression()

        self.out.write('</expressionList>\n')