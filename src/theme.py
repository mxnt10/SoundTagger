from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QStyleFactory


# Objeto para garantir o tema Breeze Dark do programa
class Theme(QObject):

    def __init__(self):
        super().__init__()
        self.__LINE__ = 150 if QPalette().color(QPalette.Window) == QColor(42, 46, 50) else 255
        self.__SELECT__ = 70 if QPalette().color(QPalette.Window) == QColor(42, 46, 50) else 50
        self.__UNSELECT__ = 20 if QPalette().color(QPalette.Window) == QColor(42, 46, 50) else 40

    # Depuração pura para visualização de cores
    @staticmethod
    def viewColors():

        colors = (
            ['QPalette.Window', QPalette.Window],
            ['QPalette.WindowText', QPalette.WindowText],
            ['QPalette.Base', QPalette.Base],
            ['QPalette.AlternateBase', QPalette.AlternateBase],
            ['QPalette.ToolTipBase', QPalette.ToolTipBase],
            ['QPalette.ToolTipText', QPalette.ToolTipText],
            ['QPalette.PlaceholderText', QPalette.PlaceholderText],
            ['QPalette.Text', QPalette.Text],
            ['QPalette.Button', QPalette.Button],
            ['QPalette.ButtonText', QPalette.ButtonText],
            ['QPalette.BrightText', QPalette.BrightText],
            ['QPalette.Light', QPalette.Light],
            ['QPalette.Midlight', QPalette.Midlight],
            ['QPalette.Dark', QPalette.Dark],
            ['QPalette.Mid', QPalette.Mid],
            ['QPalette.Shadow', QPalette.Shadow],
            ['QPalette.Highlight', QPalette.Highlight],
            ['QPalette.HighlightedText', QPalette.HighlightedText],
            ['QPalette.Link', QPalette.Link],
            ['QPalette.LinkVisited', QPalette.LinkVisited]
        )

        p = QPalette()

        for pal in colors:
            try:
                c = p.color(pal[1])
                print(f'\033[93m[{pal[0]}, QColor({c.red()}, {c.green()}, {c.blue()})]\033[m')
            except Exception as msg:
                _ = msg
                pass

    # Função para ajustes do tema claro e escuro
    @staticmethod
    def applyAutoMode() -> None:

        dark_theme = (
            [QPalette.Window, QColor(42, 46, 50)],
            [QPalette.WindowText, QColor(232, 232, 232)],
            [QPalette.Base, QColor(27, 30, 32)],
            [QPalette.AlternateBase, QColor(35, 38, 41)],
            [QPalette.ToolTipBase, QColor(49, 54, 59)],
            [QPalette.ToolTipText, QColor(232, 232, 232)],
            [QPalette.PlaceholderText, QColor(232, 232, 232)],
            [QPalette.Text, QColor(232, 232, 232)],
            [QPalette.Button, QColor(49, 54, 59)],
            [QPalette.ButtonText, QColor(232, 232, 232)],
            [QPalette.BrightText, QColor(255, 255, 255)],
            [QPalette.Light, QColor(117, 121, 126)],  # modify
            [QPalette.Midlight, QColor(54, 59, 64)],
            [QPalette.Dark, QColor(25, 27, 29)],
            [QPalette.Mid, QColor(37, 41, 44)],
            [QPalette.Shadow, QColor(18, 20, 21)],
            [QPalette.Highlight, QColor(61, 174, 233)],
            [QPalette.HighlightedText, QColor(252, 252, 252)],
            [QPalette.Link, QColor(29, 153, 243)],
            [QPalette.LinkVisited, QColor(155, 89, 182)],
        )

        light_theme = (
            [QPalette.Window, QColor(239, 240, 241)],
            [QPalette.WindowText, QColor(35, 38, 41)],
            [QPalette.Base, QColor(255, 255, 255)],
            [QPalette.AlternateBase, QColor(247, 247, 247)],
            [QPalette.ToolTipBase, QColor(247, 247, 247)],
            [QPalette.ToolTipText, QColor(35, 38, 41)],
            [QPalette.PlaceholderText, QColor(35, 38, 41)],
            [QPalette.Text, QColor(35, 38, 41)],
            [QPalette.Button, QColor(247, 247, 247)],
            [QPalette.ButtonText, QColor(35, 38, 41)],
            [QPalette.BrightText, QColor(255, 255, 255)],
            [QPalette.Light, QColor(161, 163, 164)],  # modify
            [QPalette.Midlight, QColor(246, 247, 247)],
            [QPalette.Dark, QColor(136, 142, 147)],
            [QPalette.Mid, QColor(196, 200, 204)],
            [QPalette.Shadow, QColor(71, 74, 76)],
            [QPalette.Highlight, QColor(61, 174, 233)],
            [QPalette.Link, QColor(21, 128, 185)],  # modify
            [QPalette.LinkVisited, QColor(155, 89, 182)],
        )

        p = QPalette()
        if p.color(QPalette.Window) == QColor(42, 46, 50):
            for c in dark_theme:
                p.setColor(c[0], c[1])
        elif p.color(QPalette.Window) == QColor(239, 240, 241):
            for c in light_theme:
                p.setColor(c[0], c[1])

        QApplication.setStyle(QStyleFactory.create('Breeze'))
        QApplication.setPalette(p)

    # Definir uma cor para a folha de estilo
    @staticmethod
    def color_palette(palete):
        c = QPalette().color(palete)
        return 'rgb(%s, %s, %s)' % (c.red(), c.green(), c.blue())

    # Definir uma cor semi-transparente para a folha de estilo
    @staticmethod
    def color_rgba(palete, opacy):
        c = QPalette().color(palete)
        return 'rgba(%s, %s, %s, %s)' % (c.red(), c.green(), c.blue(), str(opacy))

    # Definindo a linha dos formulários
    @staticmethod
    def color_line():
        p = QPalette()
        if p.color(QPalette.Window) == QColor(42, 46, 50):
            c = p.color(QPalette.Base)
        elif p.color(QPalette.Window) == QColor(239, 240, 241):
            c = p.color(QPalette.Light)
        else:
            return 'transparent'
        return 'rgb(%s, %s, %s)' % (c.red(), c.green(), c.blue())
