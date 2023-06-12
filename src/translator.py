from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QObject, QLocale
import os


# Classe para pesquisar o local que vai ficar a tradução
class GetLang(QObject):
    @staticmethod
    def get_lang():
        def_dir = "/usr/share/SoundTagger/lang"
        rel_dir = os.path.abspath("../lang")
        if os.path.exists(def_dir):
            return def_dir
        if os.path.exists(rel_dir):
            return rel_dir
        return os.path.abspath("lang")


# Classe para definir o idioma
class Translator(QObject):
    @staticmethod
    def translate() -> None:
        translator = QTranslator()
        if translator.load(GetLang.get_lang() + '/qt_' + QLocale.system().name().split('_')[0] + '.qm'):
            QApplication.instance().installTranslator(translator)
