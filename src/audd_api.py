from time import sleep

import requests
from PyQt5.QtCore import QObject, pyqtSignal

from settings_manager import SettingsManager

DEBUG = False

########################################################################################################################


# Objeto para o uso da API do audD.io
class audDAPI(QObject):
    finished = pyqtSignal(dict, int)
    processing = pyqtSignal(str, int)

    # Buscando informações de mídia na API
    def process(self, item, row, notificator=None) -> None:
        settings = SettingsManager()

        try:
            self.processing.emit(f'{self.tr("Searching for the music on the audD.io API")}...', row)
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
                    'api_token': str(settings.load_api_key('audD_API')),
                    'return': ''
                }
                files = {
                    'file': open(item, 'rb')
                }
                result = requests.post('https://api.audd.io/', data=data, files=files)
                self.finished.emit(result.json(), row)

        except Exception as msg:
            self.finished.emit({}, row)
            notificator.notify_send(app_title=self.tr('Error'),
                                    title=str(),
                                    message=str(msg),
                                    icon='error',
                                    timeout=10)
