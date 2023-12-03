from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox


# CheckBox customizado
class CheckBox(QCheckBox):
    def __init__(self, msg='', checked=False):
        super().__init__(msg)

        self.setFocusPolicy(Qt.NoFocus)
        self.setChecked(checked)
