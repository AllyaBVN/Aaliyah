import os


class FileHandler:
    def __init__(self, nav_folder_name='nav_files'):
        self.folder_path = self._get_folder_path(self._get_current_path(), nav_folder_name)

    def get_nav_files(self):
        raw_files = {}
        for file_name_ext in self.get_files_name_ext():
            raw_files[self._get_file_name(file_name_ext)] = self._get_raw_file(self._get_file_path(self.folder_path, file_name_ext))
        return raw_files

    def get_files_name_ext(self):
        return self._get_all_files_in_directory(self.folder_path)

    @staticmethod
    def _get_all_files_in_directory(directory_path):
        return os.listdir(directory_path)

    @staticmethod
    def _get_folder_path(current_path, folder_path):
        return os.path.join(current_path, folder_path)

    @staticmethod
    def _get_file_path(current_path, file_name):
        return os.path.join(current_path, file_name)

    @staticmethod
    def _get_current_path():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def _get_raw_file(file_path):
        with open(file_path, 'rb') as file:
            output = file.read()
        return output

    @staticmethod
    def _get_file_name(file_name_ext):
        final = ''
        for c in file_name_ext:
            if c == '.':
                return final
            final += c
        return final