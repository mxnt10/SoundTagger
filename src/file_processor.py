import tempfile

from PyQt5.QtCore import pyqtSignal, QObject

from audd_api import audDAPI
from pydub import AudioSegment
from settings_manager import SettingsManager


# Classe para auxiliar no multiprocessamento
class FileProcessor(QObject):
    return_json = pyqtSignal(dict, int)
    return_process = pyqtSignal(str, int)

    # Função para iniciar o multiprocessamento incluíndo a preparação da mídia para a busca
    def run(self, audio_path, row) -> None:
        self.return_process.emit(self.tr('Preparing File') + '...', row)
        audio = AudioSegment.from_file(audio_path)

        # Extrair parte da mídia para a pesquisa
        sett = SettingsManager()
        extracted_audio = audio[sett.load_int_config('initial_range', defaultValue=10) * 1000:
                                sett.load_int_config('final_range', defaultValue=20) * 1000]

        with tempfile.NamedTemporaryFile(suffix="." + audio_path.split(".")[-1], delete=False) as temp_file:
            temp_file = temp_file.name
            extracted_audio.export(temp_file, format=audio_path.split(".")[-1])

            audd_api = audDAPI()
            audd_api.finished.connect(lambda result, nm: self.return_json.emit(result, nm))
            audd_api.processing.connect(lambda process, nm: self.return_process.emit(process, nm))

            audd_api.process(temp_file, row)
