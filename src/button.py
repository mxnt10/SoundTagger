from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
import os


# Classe para os botões
class Button(QPushButton):
    height = pyqtSignal(QPoint)

    def __init__(self, txt, tooltip, nm=36):
        self.text = txt
        self.tooltip = tooltip
        self.nm = nm
        self.def_icon = "/usr/share/SoundTagger/icons"
        self.rel_icon = os.path.abspath("../icons")
        self.alt_icon = os.path.abspath("icons")

        super().__init__()
        self.setIcon(self.set_icon(self.text))
        self.setIconSize(QSize(self.nm, self.nm))
        self.setFixedSize(self.nm + 5, self.nm + 5)
        self.setToolTip(self.tooltip)
        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet('QPushButton { border: none; background-color: transparent; }')

    # Função para buscar ícones alternativos, caso inexistente
    @staticmethod
    def default_icon(txt):
        if txt == 'add':
            return QIcon.fromTheme('list-add')
        if txt == 'remove':
            return QIcon.fromTheme('list-remove')
        if txt == 'clean':
            return QIcon.fromTheme('dialog-cancel')
        if txt == 'remove-list':
            return QIcon.fromTheme('paint-none')
        if txt == 'run':
            return QIcon.fromTheme('run-build')
        if txt == 'main':
            return QIcon.fromTheme('go-home')
        if txt == 'settings':
            return QIcon.fromTheme('configure')
        if txt == 'about':
            return QIcon.fromTheme('help-about')
        return QIcon()

    # Função para setar os ícones
    def set_icon(self, txt):
        if os.path.exists(self.def_icon + '/' + txt + '.png'):
            return QIcon(self.def_icon + '/' + txt + '.png')
        if os.path.exists(self.rel_icon + '/' + txt + '.png'):
            return QIcon(self.rel_icon + '/' + txt + '.png')
        if os.path.exists(self.alt_icon + '/' + txt + '.png'):
            return QIcon(self.alt_icon + '/' + txt + '.png')
        return self.default_icon(txt)

    # Ação ao posicionar o mouse sobre o botão
    def enterEvent(self, event):
        self.setIconSize(QSize(self.nm + 4, self.nm + 4))
        self.height.emit(self.mapToGlobal(self.pos()))
        super().enterEvent(event)

    # Ação ao tirar o mouse sobre o botão
    def leaveEvent(self, event):
        self.setIconSize(QSize(self.nm, self.nm))
        super().leaveEvent(event)

    # Ação ao pressionar o botão
    def mousePressEvent(self, event):
        if event.button() == 1:
            self.setIconSize(QSize(self.nm + 2, self.nm + 2))
        super().mousePressEvent(event)

    # Ação ao despressionar o botão representando um clique completo
    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.setIconSize(QSize(self.nm + 4, self.nm + 4))
        super().mouseReleaseEvent(event)
