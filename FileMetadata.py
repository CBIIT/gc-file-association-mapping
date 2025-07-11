import os


class FileMetadata:

    def __init__(self, name, id):
        self.file_name = name.lower()
        self.id = id

    def get_extension(self):
        return os.path.splitext(self.file_name)[1]

    def get_file_basename(self):
        return os.path.splitext(self.file_name)[0]
