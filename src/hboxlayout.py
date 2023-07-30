from PyQt5.QtWidgets import QHBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class HBoxLayout(QHBoxLayout):
    def __init__(self, margin=5, array_widgets=None, parent=None):
        self.n = margin
        super().__init__(parent)
        self.setContentsMargins(self.n, self.n, self.n, self.n)

        if array_widgets is not None:
            for widget in array_widgets:
                if type(widget) == int:
                    self.addSpacing(widget)
                elif type(widget) == str and widget == 'S':
                    self.addStretch(1)
                else:
                    self.addWidget(widget)
