from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontDatabase, QResizeEvent
from PyQt5.QtWidgets import QWidget, QLabel

from gridlayout import GridLayout
from icon import IconPrg
from label_layout import LabelLayout
from vboxlayout import VBoxLayout

VERSION = '2023.07.27'

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

        self.desc1 = LabelLayout(d1, bold=False, one=True)
        self.desc2 = LabelLayout(d2, bold=False, one=True)
        self.desc3 = LabelLayout(d3, bold=False, one=True)
        self.desc4 = LabelLayout(d4, bold=False, one=True)

        self.desc5 = LabelLayout(self.tr('Maintainer'), 'Mauricio Ferrari', italic=False)
        self.desc6 = LabelLayout(self.tr('E-Mail'), 'm10ferrari1200@gmail.com', blue=True)
        self.desc7 = LabelLayout(self.tr('Telegram'), '@maurixnovatrento', blue=True)
        self.desc8 = LabelLayout(self.tr('License'), 'GNU General Public License Version 3 (GLPv3)', italic=False)

        lay = VBoxLayout(margin=0, spacing=0)
        lay.addStretch(1)
        lay.addLayout(self.label)
        lay.addSpacing(15)
        lay.addWidget(self.icon)
        lay.addSpacing(15)
        lay.addLayout(self.desc1)
        lay.addLayout(self.desc2)
        lay.addLayout(self.desc3)
        lay.addLayout(self.desc4)
        lay.addSpacing(15)
        lay.addLayout(self.desc5)
        lay.addLayout(self.desc6)
        lay.addLayout(self.desc7)
        lay.addSpacing(15)
        lay.addLayout(self.desc8)
        lay.addStretch(1)

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
            self.desc1.setPointSize(11)
            self.desc2.setPointSize(11)
            self.desc3.setPointSize(11)
            self.desc4.setPointSize(11)
            self.desc5.setPointSize(11)
            self.desc6.setPointSize(11)
            self.desc7.setPointSize(11)
            self.desc8.setPointSize(11)
        else:
            q = QFontDatabase.systemFont(QFontDatabase.GeneralFont).pointSize()
            self.desc1.setPointSize(q)
            self.desc2.setPointSize(q)
            self.desc3.setPointSize(q)
            self.desc4.setPointSize(q)
            self.desc5.setPointSize(q)
            self.desc6.setPointSize(q)
            self.desc7.setPointSize(q)
            self.desc8.setPointSize(q)
