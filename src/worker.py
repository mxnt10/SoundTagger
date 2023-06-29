from PyQt5.QtCore import QRunnable


# classe para auxiliar no pool de processos
class Worker(QRunnable):
    def __init__(self, file_processor, file_name, row):
        super().__init__()
        self.file_processor = file_processor
        self.file_name = file_name
        self.row = row

    # Iniciar worker
    def run(self) -> None:
        self.file_processor.run(self.file_name, self.row)
