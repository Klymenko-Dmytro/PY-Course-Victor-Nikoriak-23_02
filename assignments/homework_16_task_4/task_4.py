class Custom_Exception(Exception):

    def __init__(self, msg):
        self.msg = msg

    def write_error(self, msg):
        with open('logs.txt', 'a') as f:
            f.write(msg + '\n')


errors_msg = Custom_Exception('Error message')

try:
    raise TypeError('Errors!')
except TypeError as e:
    errors_msg.write_error(str(e))


