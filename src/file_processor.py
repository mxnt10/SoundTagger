from PyQt5.QtCore import pyqtSignal, QObject, QRunnable
from audd_api import audDAPI
from pydub import AudioSegment
import tempfile


class FileProcessor(QObject):
    return_json = pyqtSignal(dict, int)
    return_process = pyqtSignal(str, int)

    def run(self, audio_path, row) -> None:
        audio = AudioSegment.from_file(audio_path)
        extracted_audio = audio[10000:20000]

        with tempfile.NamedTemporaryFile(suffix="." + audio_path.split(".")[-1], delete=False) as temp_file:
            temp_file = temp_file.name
            extracted_audio.export(temp_file, format=audio_path.split(".")[-1])

            audd_api = audDAPI()
            audd_api.finished.connect(lambda result, nm: self.return_json.emit(result, nm))
            audd_api.processing.connect(lambda process, nm: self.return_process.emit(process, nm))

            audd_api.process(temp_file, row)


class Worker(QRunnable):
    def __init__(self, file_processor, file_name, row):
        super().__init__()
        self.file_processor = file_processor
        self.file_name = file_name
        self.row = row

    def run(self) -> None:
        self.file_processor.run(self.file_name, self.row)
