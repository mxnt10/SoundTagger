from PyQt5.QtWidgets import QVBoxLayout


# Customização do layout para personalizar a interface mais facilmente
class VBoxLayout(QVBoxLayout):
    def __init__(self, parent=None, margin=5, spacing=5, array_widgets=None):
        self.n = margin
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

        if array_widgets is not None:
            for widget in array_widgets:
                self.addWidget(widget)
