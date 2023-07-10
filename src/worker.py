from PyQt5.QtCore import QRunnable, pyqtSignal, QObject


# classe para auxiliar no pool de processos
class Worker(QRunnable):
    def __init__(self, file_processor, file_name, row, shared_class=None):
        super().__init__()
        self.file_processor = file_processor
        self.file_name = file_name
        self.row = row
        self.callback = shared_class

    # Iniciar worker
    def run(self) -> None:
        self.file_processor.run(self.file_name, self.row, self.callback)


# Classe compartilhada para fazer a emissão dos sinais para
class SharedClass(QObject):
    emitting = pyqtSignal(dict, int)

    def emit(self, json, key) -> None:
        self.emitting.emit(json, key)
