import threading

import acoustid
from PyQt5.QtCore import pyqtSignal, QObject

from settings_manager import SettingsManager
from notification import Notification


class AcoustIDAPI(QObject):
    processing = pyqtSignal(str, int)

    def process(self, item, row, callback=None) -> None:
        self.processing.emit(self.tr('Searching for the music on the AcoustID API...'), row)

        thread = threading.Thread(target=self.result_thread, args=(item, row, callback))
        thread.start()

    # Função para usar em um thread independente
    def result_thread(self, item, row, callback) -> None:
        settings = SettingsManager()
        try:
            result_json = {'status': 'success',
                           'result': None}
            results = acoustid.match(settings.load_api_key('acoustID_API'), item)

            for score, rid, title, artist in results:
                if artist is None or title is None:
                    continue
                result_json = {'status': 'success',
                               'result': {'artist': artist, 'title': title, 'score': str(int(score * 100)) + '%',
                                          'song_link': 'http://musicbrainz.org/recording/' + rid}}
                break

            callback.emit(result_json, row)

        except acoustid.NoBackendError:
            Notification().notify_send(app_title=self.tr('Error'),
                                       title=self.tr('Dependency Error'),
                                       message=self.tr('Chromaprint library/tool not found.'),
                                       icon='error',
                                       timeout=10)
            callback.emit({}, row)
        except acoustid.FingerprintGenerationError:
            Notification().notify_send(app_title=self.tr('Error'),
                                       title=self.tr('Fingerprint Generation Error'),
                                       message=self.tr('Fingerprint could not be calculated.'),
                                       icon='error',
                                       timeout=10)
            callback.emit({}, row)
        except acoustid.WebServiceError as exc:
            Notification().notify_send(app_title=self.tr('Error'),
                                       title=self.tr('Web Service Error'),
                                       message=self.tr('Web service request failed' + ': ' + exc.message),
                                       icon='error',
                                       timeout=10)
            callback.emit({}, row)