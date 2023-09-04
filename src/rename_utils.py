import os

from PyQt5.QtCore import QObject


# Classe para opções para renomeação de arquivos de mídia
class RenameUtils(QObject):
    def __init__(self):
        super().__init__()

    # Função para renomear os arquivos
    @staticmethod
    def rename_file(file_path, title):
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        new_file_name = f'{title}{extension}'
        new_file_name = new_file_name.replace(';', ',')
        new_file_path = os.path.join(dir_name, new_file_name)

        try:
            os.rename(file_path, new_file_path)
            return new_file_path
        except OSError:
            return file_path
