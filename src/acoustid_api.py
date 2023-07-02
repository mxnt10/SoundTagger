import sys
import threading

import acoustid
from PyQt5.QtCore import pyqtSignal, QObject

from settings_manager import SettingsManager


class AcoustIDAPI(QObject):
    processing = pyqtSignal(str, int)

    def process(self, item, row, comp) -> None:
        self.processing.emit(self.tr('Searching for the music on the AcoustID API...'), row)

        thread = threading.Thread(target=self.result_thread, args=(item, row, comp))
        thread.start()

    # Função para usar em um thread independente
    @staticmethod
    def result_thread(item, row, callback) -> None:
        settings = SettingsManager()
        try:
            result_json = {'status': 'success',
                           'result': None}
            results = acoustid.match(str(settings.load_api_key('acoustID_API')), item)

            for score, rid, title, artist in results:
                if artist is None or title is None:
                    continue
                result_json = {'status': 'success',
                               'result': {'artist': artist, 'title': title, 'score': str(int(score * 100)) + '%',
                                          'song_link': 'http://musicbrainz.org/recording/' + rid}}
                break

            callback.emit(result_json, row)

        except acoustid.NoBackendError:
            print("chromaprint library/tool not found", file=sys.stderr)
            callback.emit({}, row)
        except acoustid.FingerprintGenerationError:
            print("fingerprint could not be calculated", file=sys.stderr)
            callback.emit({}, row)
        except acoustid.WebServiceError as exc:
            print("web service request failed:", exc.message, file=sys.stderr)
            callback.emit({}, row)
