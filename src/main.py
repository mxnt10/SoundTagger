import sys

from PyQt5.QtGui import QMouseEvent, QResizeEvent, QCloseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QStackedWidget

from about import About
from background import Background
from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from icon import IconPrg
from list import ListWidget
from notification import Notification
from run_options import RunOptions
from settings import Settings
from settings_manager import SettingsManager
from theme import Theme
from translator import Translator
from vboxlayout import VBoxLayout

########################################################################################################################


# Classe da interface principal
class SoundTaggerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SoundTagger')
        self.setWindowIcon(IconPrg.get_icon())
        self.setMinimumSize(640, 460)
        self.setStyleSheet(Background().get_background())

        # Widget da interface principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Definição e ajuste da lista
        self.run_options = RunOptions()
        list_widget = ListWidget()
        list_widget.setWidgetEvent(self.run_options)
        list_widget.added.connect(self.activeButtons)
        list_widget.removed.connect(self.deactiveButtons)
        list_layout = HBoxLayout(margin=9, array_widgets=[list_widget])
        self.run_options.run.connect(list_widget.process_sounds)

        # Widget da lista para o QStackedWidget
        table = QWidget()
        layout_list = GridLayout(parent=table, margin=0)
        layout_list.addLayout(list_layout, 0, 0)

        # Widgets de configuração e sobre
        about_widget = About()
        settings_widget = Settings()

        # Lista de widgets para sobreposição
        self.stack = QStackedWidget()
        self.stack.addWidget(table)
        self.stack.addWidget(about_widget)
        self.stack.addWidget(settings_widget)

        # Botões da interface
        self.add = Button('add', tooltip=self.tr('Add Files'))
        self.add.clicked.connect(list_widget.add_item)
        self.remove = Button('remove', tooltip=self.tr('Remove File'))
        self.remove.clicked.connect(list_widget.remove_selected_items)
        self.clean = Button('clean', tooltip=self.tr('Remove Selected Files'))
        self.clean.clicked.connect(list_widget.clear_items)
        self.run = Button('fingerprint', tooltip=self.tr('Search Music Information'))
        self.run.height.connect(self.run_options.set_point)
        self.run.clicked.connect(self.show_options)
        main = Button('return', tooltip=self.tr('Return to Main'))
        main.clicked.connect(self.get_main)
        settings = Button('settings', tooltip=self.tr('Settings'))
        settings.clicked.connect(self.get_settings)
        about = Button('about', tooltip=self.tr('About'))
        about.clicked.connect(self.get_about)
        self.deactiveButtons()

        # Controle do botão main
        self.v_main = QWidget()
        self.v_main.setVisible(False)
        v_main_layout = GridLayout(parent=self.v_main)
        v_main_layout.addLayout(HBoxLayout(array_widgets=[main]), 0, 0)

        # Ajuste dos botões do menu principal
        self.v_buttons = QWidget()
        list_buttons_layout = GridLayout(parent=self.v_buttons)
        list_buttons_layout.addLayout(HBoxLayout(array_widgets=[self.add, self.remove,
                                                                self.clean, 10, self.run]), 0, 0)

        # Ajuste dos botões e layout
        f_buttons = QWidget()
        f_buttons_layout = GridLayout(parent=f_buttons)
        f_buttons_layout.addLayout(HBoxLayout(array_widgets=[settings, about]), 0, 0)
        buttons = HBoxLayout(margin=0, array_widgets=[self.v_buttons, 'S', self.v_main, f_buttons])

        # Layout principal
        main_layout = VBoxLayout(parent=main_widget)
        main_layout.addLayout(GridLayout(margin=0, layout=buttons))
        main_layout.addWidget(self.stack)

        # Centralizar a janela
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    # Painel principal
    def get_main(self) -> None:
        self.stack.setCurrentIndex(0)
        self.v_buttons.setVisible(True)
        self.v_main.setVisible(False)

    # Painel sobre
    def get_about(self) -> None:
        self.stack.setCurrentIndex(1)
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)

    # Painel de configurações
    def get_settings(self) -> None:
        self.stack.setCurrentIndex(2)
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)

    def show_options(self):
        s = SettingsManager()
        if s.priority_api() is not None:
            self.run_options.show()
        else:
            Notification().notify_send(app_title=self.tr('Information'),
                                       title=self.tr('Configure an API Key'),
                                       message=self.tr('No API Key has been configured!'),
                                       icon='key')

    # Ativar botões
    def activeButtons(self):
        self.remove.setVisible(True)
        self.clean.setVisible(True)
        self.run.setVisible(True)

    # Desativar botões
    def deactiveButtons(self):
        self.remove.setVisible(False)
        self.clean.setVisible(False)
        self.run.setVisible(False)

    # Por enquanto vai servir
    def moveEvent(self, event):
        if not self.run_options.isHidden():
            self.run_options.set_resize(self.run.mapToGlobal(self.run.pos()))

    # Ação ao redirecionar a janela, o diágolo de opções pode variar de posição
    def resizeEvent(self, event: QResizeEvent) -> None:
        if not self.run_options.isHidden():
            self.run_options.set_resize(self.run.mapToGlobal(self.run.pos()))

    # Para fechar o diálogo ao clicar na interface
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if not self.run_options.isHidden():
            self.run_options.close()
        super().mouseReleaseEvent(event)

    # Se tiver algo pendente, finalizar
    def closeEvent(self, event: QCloseEvent) -> None:
        self.run_options.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Theme.applyDarkMode()
    Translator().translate()

    sound_tagger = SoundTaggerApp()
    sound_tagger.show()
    sys.exit(app.exec_())
