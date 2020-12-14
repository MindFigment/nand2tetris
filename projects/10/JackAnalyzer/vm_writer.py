class VMWriter(object):
    """
    lalala
    """

    def __init__(self, output_file):
        self.out = open(output_file, 'w')


    def write_push(self, segment, index):
        lines_to_write = self._write_two_arg('push', segment, index)
        self._write_to_out(lines_to_write)


    def write_pop(self, segment, index):
        lines_to_write = self._write_two_arg('pop', segment, index)
        self._write_to_out(lines_to_write)


    def write_arithmetic(self, command):
        lines_to_write = [command]
        self._write_to_out(lines_to_write)


    def write_label(self, label):
        lines_to_write = self._write_one_arg('label', label)
        self._write_to_out(lines_to_write)


    def write_goto(self, label):
        lines_to_write = self._write_one_arg('goto', label)
        self._write_to_out(lines_to_write)


    def write_if(self, label):
        lines_to_write = self._write_one_arg('if-goto', label)
        self._write_to_out(lines_to_write)


    def write_call(self, name, n_args):
        lines_to_write = self._write_two_arg('call', name, n_args)
        self._write_to_out(lines_to_write)


    def write_function(self, name, n_locals):
        lines_to_write = self._write_two_arg('function', name, n_locals)
        self._write_to_out(lines_to_write)


    def write_return(self):
        lines_to_write = ['return']
        self._write_to_out(lines_to_write)


    def close(self):
        if self.out:
            self.out.close()
            self.out = None


    def _write_to_out(self, lines_to_write):
        for line in lines_to_write:
            self.out.write(line + '\n')


    def _write_one_arg(self, name, arg):
        lines_to_write = [
            '{} {}'.format(name, arg)
        ]
        return lines_to_write

    
    def _write_two_arg(self, name, arg1, arg2):
        lines_to_write = [
            '{} {} {}'.format(name, arg1, arg2)
        ]
        return lines_to_write