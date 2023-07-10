from PyQt5.QtWidgets import QHBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class HBoxLayout(QHBoxLayout):
    def __init__(self, margin=5, array_widgets=None):
        self.n = margin
        super().__init__()
        self.setContentsMargins(self.n, self.n, self.n, self.n)

        if array_widgets is not None:
            for widget in array_widgets:
                self.addWidget(widget)
