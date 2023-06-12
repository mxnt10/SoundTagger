from PyQt5.QtWidgets import QHBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class HBoxLayout(QHBoxLayout):
    def __init__(self, n=5):
        self.n = n
        super().__init__()
        self.setContentsMargins(self.n, self.n, self.n, self.n)
