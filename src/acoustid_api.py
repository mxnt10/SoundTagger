import threading

from PyQt5.QtCore import pyqtSignal, QObject

from settings_manager import SettingsManager
import acoustid

########################################################################################################################


class AcoustIDAPI(QObject):
    processing = pyqtSignal(str, int)

    def process(self, item, row, callback=None, notificator=None) -> None:
        self.processing.emit(f'{self.tr("Searching for the music on the AcoustID API")}...', row)

        thread = threading.Thread(target=self.result_thread, args=(item, row, callback, notificator))
        thread.start()

    # Função para usar em um thread independente
    def result_thread(self, item, row, callback, notificator) -> None:
        settings = SettingsManager()
        try:
            result_json = {'status': 'success', 'result': None}
            results = acoustid.match(settings.load_api_key('acoustID_API'), item)

            for score, rid, title, artist in results:
                if artist is None or title is None:
                    continue
                result_json = {'status': 'success',
                               'result': {'artist': artist, 'title': title, 'score': f'{str(int(score * 100))}%',
                                          'song_link': f'http://musicbrainz.org/recording/{rid}'}}
                break

            callback.emit(result_json, row)

        except acoustid.NoBackendError:
            callback.emit({}, row)
            notificator.notify_send(app_title=self.tr('Error'),
                                    title=self.tr('Dependency Error'),
                                    message=self.tr('Chromaprint library/tool not found.'),
                                    icon='error',
                                    timeout=10)
        except acoustid.FingerprintGenerationError:
            callback.emit({}, row)
            notificator.notify_send(app_title=self.tr('Error'),
                                    title=self.tr('Fingerprint Generation Error'),
                                    message=self.tr('Fingerprint could not be calculated.'),
                                    icon='error',
                                    timeout=10)
        except acoustid.WebServiceError as exc:
            callback.emit({}, row)
            notificator.notify_send(app_title=self.tr('Error'),
                                    title=self.tr('Web Service Error'),
                                    message=f'{self.tr("Web service request failed")}: {exc.message}',
                                    icon='error',
                                    timeout=10)
