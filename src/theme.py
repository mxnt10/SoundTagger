from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QStyleFactory


# Objeto para garantir o tema Breeze Dark do programa
class Theme(QObject):
    @staticmethod
    def applyDarkMode() -> None:
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(42, 46, 50))
        dark_palette.setColor(QPalette.WindowText, QColor(252, 252, 252))
        dark_palette.setColor(QPalette.Base, QColor(27, 30, 32))
        dark_palette.setColor(QPalette.AlternateBase, QColor(27, 30, 32, 128))  # Semitransparente
        dark_palette.setColor(QPalette.ToolTipBase, QColor(49, 54, 59))
        dark_palette.setColor(QPalette.ToolTipText, QColor(252, 252, 252))
        dark_palette.setColor(QPalette.Text, QColor(252, 252, 252))
        dark_palette.setColor(QPalette.Button, QColor(42, 46, 50))
        dark_palette.setColor(QPalette.ButtonText, QColor(252, 252, 252))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Link, QColor(29, 153, 243))
        dark_palette.setColor(QPalette.Highlight, QColor(61, 174, 233))
        dark_palette.setColor(QPalette.HighlightedText, QColor(252, 252, 252))

        QApplication.setStyle(QStyleFactory.create('Breeze'))
        QApplication.setPalette(dark_palette)