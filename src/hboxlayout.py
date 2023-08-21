from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class HBoxLayout(QHBoxLayout):
    def __init__(self, margin=5, array_widgets=None, parent=None, space=5):
        super().__init__(parent)
        self.setSpacing(space)

        if isinstance(margin, QMargins):
            self.setContentsMargins(margin)
        else:
            self.setContentsMargins(margin, margin, margin, margin)

        if array_widgets is not None:
            for widget in array_widgets:
                if type(widget) == int:
                    self.addSpacing(widget)
                elif type(widget) == str and widget == 'S':
                    self.addStretch(1)
                else:
                    if isinstance(widget, QHBoxLayout) or isinstance(widget, QVBoxLayout):
                        self.addLayout(widget)
                    else:
                        self.addWidget(widget)
