import os

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon


# Classe para definir o ícone do programa
class IconPrg(QObject):

    # Função estática que define o ícone
    @staticmethod
    def get_icon(string=False):
        def_icon = '/usr/share/pixmaps/SoundTagger.png'
        rel_icon = f'{os.path.abspath("../common")}/SoundTagger.png'
        alt_icon = f'{os.path.abspath("common")}/SoundTagger.png'
        if os.path.exists(def_icon):
            if string:
                return def_icon
            return QIcon(def_icon)
        if os.path.exists(rel_icon):
            if string:
                return rel_icon
            return QIcon(rel_icon)
        if os.path.exists(alt_icon):
            if string:
                return alt_icon
            return QIcon(alt_icon)
        if string:
            return ''
        return QIcon()
