import os

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPoint, QEvent
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap, QPainter
from PyQt5.QtWidgets import QPushButton

__SELECT__ = 5
__CLICK__ = 3
__AJUST__ = 4
__SIZE__ = 52
__ALPHA__ = 180
__CLK_ALPHA__ = 200

########################################################################################################################


# Classe para os botões
class Button(QPushButton):
    height = pyqtSignal(QPoint)

    def __init__(self, text, tooltip='', size=__SIZE__, ajust=__AJUST__, select=__SELECT__, click=__CLICK__):
        self.text = text
        self.nm = size
        self.sel = select
        self.clk = click
        self.def_icon = "/usr/share/SoundTagger/icons"
        self.rel_icon = os.path.abspath("../icons")
        self.alt_icon = os.path.abspath("icons")

        super().__init__()
        self.icon = self.set_icon(self.text)

        self.setIcon(self.contrastIcon(self.icon, self.nm))
        self.setIconSize(QSize(self.nm, self.nm))
        self.setFixedSize(self.nm - ajust, self.nm - ajust)
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet(
            'QPushButton {'
            '    border: none;'
            '    background-color: transparent;'
            '}'
        )

########################################################################################################################

    # Função para buscar ícones alternativos, caso inexistente
    @staticmethod
    def defaultIcon(txt):
        if txt == 'add':
            return QIcon.fromTheme('list-add')
        if txt == 'remove':
            return QIcon.fromTheme('list-remove')
        if txt == 'clean':
            return QIcon.fromTheme('dialog-cancel')
        if txt == 'remove-list':
            return QIcon.fromTheme('paint-none')
        if txt == 'fingerprint':
            return QIcon.fromTheme('run-build')
        if txt == 'return':
            return QIcon.fromTheme('go-home')
        if txt == 'settings':
            return QIcon.fromTheme('configure')
        if txt == 'about':
            return QIcon.fromTheme('help-about')
        if txt == 'apply':
            return QIcon.fromTheme('run-build')
        return QIcon()

    # Função para setar os ícones
    def set_icon(self, txt):
        ext = 'svg'
        if os.path.exists(f'{self.def_icon}/{txt}.{ext}'):
            return QIcon(f'{self.def_icon}/{txt}.{ext}')
        if os.path.exists(f'{self.rel_icon}/{txt}.{ext}'):
            return QIcon(f'{self.rel_icon}/{txt}.{ext}')
        if os.path.exists(f'{self.alt_icon}/{txt}.{ext}'):
            return QIcon(f'{self.alt_icon}/{txt}.{ext}')
        return self.defaultIcon(txt)

    # Ajuste do contraste do ícone conforme o tema
    def contrastIcon(self, icon, size, alpha=__ALPHA__):
        themed_pixmap = QPixmap(size, size)
        themed_pixmap.fill(Qt.transparent)

        # Desenhe o ícone original em tons de cinza
        painter = QPainter(themed_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, QPixmap(icon.pixmap(size, size)))

        # Pinte o ícone com a cor do tema
        color = self.palette().color(self.foregroundRole())
        color.setAlpha(alpha)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(themed_pixmap.rect(), color)
        painter.end()

        return QIcon(themed_pixmap)

########################################################################################################################

    # Ação ao posicionar o mouse sobre o botão
    def enterEvent(self, event: QEvent) -> None:
        self.setIcon(self.contrastIcon(self.icon, self.nm + self.sel, alpha=__CLK_ALPHA__))
        self.setIconSize(QSize(self.nm + self.sel, self.nm + self.sel))
        self.height.emit(self.pos())
        super().enterEvent(event)

    # Ação ao tirar o mouse sobre o botão
    def leaveEvent(self, event: QEvent) -> None:
        self.setIcon(self.contrastIcon(self.icon, self.nm))
        self.setIconSize(QSize(self.nm, self.nm))
        super().leaveEvent(event)

    # Ação ao pressionar o botão
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == 1:
            self.setIcon(self.contrastIcon(self.icon, self.nm + self.clk, alpha=__CLK_ALPHA__))
            self.setIconSize(QSize(self.nm + self.clk, self.nm + self.clk))
        super().mousePressEvent(event)

    # Ação ao despressionar o botão representando um clique completo
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == 1:
            self.setIcon(self.contrastIcon(self.icon, self.nm + self.sel, alpha=__CLK_ALPHA__))
            self.setIconSize(QSize(self.nm + self.sel, self.nm + self.sel))
        super().mouseReleaseEvent(event)
