class SymbolTable(object):
    """
    lalala
    """

    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}

        #############
        ### KINDS ###
        #############

        self.static_kind = 'static'
        self.field_kind = 'field'
        self.argument_kind = 'argument'
        self.local_kind = 'local'
        self.var_kind = 'var'

        #############
        ### TYPES ###
        #############

        self.int_type = 'int'
        self.string_type = 'String'
        self.boolean_type = 'boolean'

        self.running_idxs = {
            self.static_kind: 0,
            self.field_kind: 0,
            self.argument_kind: 0,
            self.local_kind: 0
        }


    def start_subroutine(self):
        self.subroutine_table = {}
        self.running_idxs = {
            self.static_kind: 0,
            self.field_kind: 0,
            self.argument_kind: 0,
            self.local_kind: 0
        }

    
    def define(self, name, type_, kind):
        if kind in [self.argument_kind, self.local_kind]:
            self.subroutine_table[name] = {
                'type': type_,
                'kind': kind,
                'idx': self.running_idxs[kind]
            }

            self.running_idxs[kind] += 1

        elif kind in [self.static_kind, self.field_kind]:
            self.class_table[name] = {
                'type': type_,
                'kind': kind,
                'idx': self.running_idxs[kind]
            }

            self.running_idxs[kind] += 1

        else:
            raise ValueError('Cannot recognize kind argument: {}'.format(kind))
        

    def var_count(self, kind):
        var_count = len([v for v, k in self.subroutine_table.items() if k[kind] == self.var_kind])
        return var_count

    
    def kind_of(self, name):
        return self._xxx_of('kind', name)

    
    def type_of(self, name):
        return self._xxx_of('type', name)


    def index_of(self, name):
        return self._xxx_of('idx', name)


    def _xxx_of(self, what, name):
        if name in self.subroutine_table:
            return self.subroutine_table[name][what]
        else:
            if name in self.class_table:
                return self.class_table[name][what]
            else:
                return None
            