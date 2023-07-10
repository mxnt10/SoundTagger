import os

from PyQt5.QtCore import QObject

from mutagen.easyid3 import EasyID3


# Classe para taggear as músicas e renomear se possível
class MusicUtils(QObject):
    def __init__(self):
        super().__init__()

    # Função para editar as tags
    @staticmethod
    def apply_tags(file_path, artist, title, album) -> None:
        audio = EasyID3(file_path)
        if title is not None:
            audio['title'] = title
        if artist is not None:
            audio['artist'] = artist
        if album is not None:
            audio['album'] = album
        audio.save()

    # Função para renomear os arquivos
    @staticmethod
    def rename_file(file_path, title):
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        new_file_name = f'{title}{extension}'
        new_file_name = new_file_name.replace(';', ' ft.')
        new_file_path = os.path.join(dir_name, new_file_name)

        try:
            os.rename(file_path, new_file_path)
            return new_file_path
        except OSError:
            return file_path
