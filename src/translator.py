import os

from PyQt5.QtCore import QTranslator, QObject, QLocale
from PyQt5.QtWidgets import QApplication


# Classe para definir o idioma
class Translator(QObject):

    # Local onde estão os idiomas
    @staticmethod
    def get_lang():
        def_dir = "/usr/share/SoundTagger/lang"
        rel_dir = os.path.abspath("../lang")
        if os.path.exists(def_dir):
            return def_dir
        if os.path.exists(rel_dir):
            return rel_dir
        return os.path.abspath("lang")

    # Função para aplicar o idioma
    def translate(self) -> None:
        translator = QTranslator()
        if translator.load(self.get_lang() + '/qt_' + QLocale.system().name().split('_')[0] + '.qm'):
            QApplication.instance().installTranslator(translator)
