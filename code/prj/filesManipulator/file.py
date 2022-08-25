import os


class File:
    def __init__(self, path):
        self.path = "../" + path

    def write(self, lines):
        """
        :param lines: deve ser uma lista
        :return: não retorna nada
        """
        with open(self.path, 'a', encoding='utf-8') as file:
            file.writelines(lines)

    def read(self):
        with open(self.path) as f:
            lines = f.readlines()
        return lines

    @staticmethod
    def remove_file(path):
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
            print("file '" + path + "' has been deleted")
        else:
            print("file '" + path + "' not found")






"""
f = File(".user.ini")
f.write("max_input_vars = 1000000")
"""

