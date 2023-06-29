from PyQt5.QtWidgets import QVBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class VBoxLayout(QVBoxLayout):
    def __init__(self, parent=None, n=5):
        self.n = n
        super().__init__(parent)
        self.setContentsMargins(self.n, self.n, self.n, self.n)