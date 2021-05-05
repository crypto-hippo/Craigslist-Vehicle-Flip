
class DDLogger(object):

    """ Logger for writing data to files and standard output """
    def __init__(self, filename="crawler.debug.log"):
        self.filename = filename
        self.file = open(self.filename, 'w')

    def open_file(self):
        self.file = open(self.filename, 'w')
        
    def write_to_file(self, content):
        self.file.write(content)

    def close_and_delete_file(self):
        self.file.close()
        del self.file

        
        