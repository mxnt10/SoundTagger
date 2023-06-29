from time import sleep

import requests
from PyQt5.QtCore import QObject, pyqtSignal

from settings_manager import SettingsManager

DEBUG = False


# Objeto para o uso da API do audD.io
class audDAPI(QObject):
    finished = pyqtSignal(dict, int)
    processing = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

    def process(self, item, row) -> None:
        settings = SettingsManager()

        try:
            self.processing.emit(self.tr('Searching for the music on the audD.io API...'), row)
            if DEBUG:  # Mais rápido que a requisição, para testes rápidos

                sleep(1)
                result = {'status': 'success',
                          'result': {'artist': 'Ak9', 'title': 'Blue Sky', 'album': 'Blue Sky',
                                     'release_date': '2016-07-01',
                                     'label': 'Kontor Records', 'timecode': '03:41',
                                     'song_link': 'https://lis.tn/BNAEUF'}}
                self.finished.emit(result, row)

            else:

                data = {
                    'api_token': str(settings.load_audd_api_key()),  # fixme
                    'return': '',
                }
                files = {
                    'file': open(item, 'rb'),  # fixme
                }
                result = requests.post('https://api.audd.io/', data=data, files=files)
                self.finished.emit(result.json(), row)

        except Exception as msg:
            self.processing.emit(self.tr('Error') + ': ' + str(msg), row)
