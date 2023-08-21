from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontDatabase, QResizeEvent
from PyQt5.QtWidgets import QWidget, QLabel

from gridlayout import GridLayout
from icon import IconPrg
from label_layout import LabelLayout
from vboxlayout import VBoxLayout

VERSION = '23.08.20'

# Software que usa uma API de impressão digital acústica para buscar metadados
# de arquivos multimídia como artista, título e álbum.
# Além disso, possui configurações para automatizar tarefas como renomear arquivos multimídia
# de acordo com o resultado da pesquisa e editar as ID tags.

########################################################################################################################


# Classe para as informações do programa
class About(QWidget):
    def __init__(self):
        super().__init__()

        self.label = LabelLayout('SoundTagger ' + self.tr('Version') + ' ' + VERSION, pointsize=12, one=True)

        self.icon = QLabel()
        self.pixmap = QPixmap(IconPrg.get_icon(string=True))
        self.icon.setPixmap(self.pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        d1 = self.tr('Software that uses an acoustic fingerprint API to fetch multimedia')
        d2 = self.tr('file metadata such as artist, title, and album.')
        d3 = self.tr('Furthermore, it has settings to automate tasks such as renaming multimedia')
        d4 = self.tr('files according to the search result and editing ID tags.')

        desc1 = LabelLayout(d1, bold=False, one=True)
        desc2 = LabelLayout(d2, bold=False, one=True)
        desc3 = LabelLayout(d3, bold=False, one=True)
        desc4 = LabelLayout(d4, bold=False, one=True)

        desc5 = LabelLayout(self.tr('Maintainer'), 'Mauricio Ferrari', italic=False)
        desc6 = LabelLayout(self.tr('E-Mail'), 'm10ferrari1200@gmail.com', blue=True)
        desc7 = LabelLayout(self.tr('Telegram'), '@maurixnovatrento', blue=True)
        desc8 = LabelLayout(self.tr('License'), 'GNU General Public License Version 3 (GLPv3)', italic=False)

        self.it = ['S', self.label, 15, self.icon, 15, desc1, desc2, desc3, desc4, 15,
                   desc5, desc6, desc7, 15, desc8, 'S']

        lay = VBoxLayout(margin=0, spacing=0, array_widgets=self.it)

        # Centralizando os widgets no layout
        for i in range(lay.count()):
            item = lay.itemAt(i)
            item.setAlignment(Qt.AlignCenter)

        self.setLayout(GridLayout(margin=0, layout=lay))

########################################################################################################################

    def resizeEvent(self, event: QResizeEvent) -> None:
        s = int(self.size().height() / 4)
        self.icon.setPixmap(self.pixmap.scaled(s, s, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        f = int(self.size().height() / 50)
        if 12 < f < 19:
            self.label.setPointSize(f)
        elif f < 19:
            self.label.setPointSize(12)

        if f > 15:
            for i in self.it:
                if i == self.label:
                    continue
                if isinstance(i, LabelLayout):
                    i.setPointSize(11)
        else:
            q = QFontDatabase.systemFont(QFontDatabase.GeneralFont).pointSize()
            for i in self.it:
                if i == self.label:
                    continue
                if isinstance(i, LabelLayout):
                    i.setPointSize(q)
