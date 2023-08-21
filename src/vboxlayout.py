from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class VBoxLayout(QVBoxLayout):
    def __init__(self, parent=None, margin=5, spacing=5, array_widgets=None):
        self.n = margin
        super().__init__(parent)
        self.setSpacing(spacing)

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
