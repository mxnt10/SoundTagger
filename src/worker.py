from PyQt5.QtCore import QRunnable, pyqtSignal, QObject


# classe para auxiliar no pool de processos
class Worker(QRunnable):
    def __init__(self, file_processor, file_name, row, shared_class=None, notificator=None):
        super().__init__()
        self.file_processor = file_processor
        self.file_name = file_name
        self.row = row
        self.callback = shared_class
        self.notify = notificator

    # Iniciar worker
    def run(self) -> None:
        self.file_processor.run(self.file_name, self.row, self.callback, self.notify)


# Classe compartilhada para fazer a emissão dos sinais
class SharedClass(QObject):
    emitting = pyqtSignal(dict, int)

    # A emissão compartilhada
    def emit(self, json, key) -> None:
        self.emitting.emit(json, key)
