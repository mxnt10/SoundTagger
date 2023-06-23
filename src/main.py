from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QDesktopWidget, QStackedWidget

from about import About
from background import Background
from button import Button
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from icon import IconPrg
from list import ListWidget
from settings import Settings
from translator import Translator
from theme import Theme
from run_options import RunOptions

import sys


# Classe da interface principal
class SoundTaggerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SoundTagger')
        self.setWindowIcon(IconPrg.get_icon())
        self.setMinimumSize(600, 400)
        self.setStyleSheet(Background().get_background())

        # Widget da interface principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Definição e ajuste da lista
        self.run_options = RunOptions()
        list_widget = ListWidget()
        list_widget.setWidgetEvent(self.run_options)
        list_layout = HBoxLayout(9)
        list_layout.addWidget(list_widget)
        self.run_options.run.connect(list_widget.process_sounds)

        # Widget da lista para o QStackedWidget
        table = QWidget()
        layout_list = GridLayout(table, 0)
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
        add = Button('add', self.tr('Add Files'))
        add.clicked.connect(list_widget.add_item)
        remove = Button('remove', self.tr('Remove File'))
        remove.clicked.connect(list_widget.remove_selected_items)
        clean = Button('clean', self.tr('Remove Selected Files'))
        clean.clicked.connect(list_widget.clear_items)
        self.run = Button('run', self.tr('Run Process'))
        self.run.height.connect(self.run_options.set_point)
        self.run.clicked.connect(self.run_options.show)
        main = Button('main', self.tr('Return to Main'))
        main.clicked.connect(self.get_main)
        settings = Button('settings', self.tr('Settings'))
        settings.clicked.connect(self.get_settings)
        about = Button('about', self.tr('About'))
        about.clicked.connect(self.get_about)

        # Ajuste do botão main
        return_main = HBoxLayout()
        return_main.addWidget(main)

        # Controle do botão main
        self.v_main = QWidget()
        self.v_main.setVisible(False)
        v_main_layout = GridLayout(self.v_main)
        v_main_layout.addLayout(return_main, 0, 0)

        # Botões do menu principal
        list_buttons = HBoxLayout()
        list_buttons.addWidget(add)
        list_buttons.addWidget(remove)
        list_buttons.addWidget(clean)
        list_buttons.addWidget(self.run)

        # Ajuste dos botões
        self.v_buttons = QWidget()
        list_buttons_layout = GridLayout(self.v_buttons)
        list_buttons_layout.addLayout(list_buttons, 0, 0)

        # Botões de configuração e sobre
        fixed_buttons = HBoxLayout()
        fixed_buttons.addWidget(settings)
        fixed_buttons.addWidget(about)

        # Ajuste dos botões
        f_buttons = QWidget()
        f_buttons_layout = GridLayout(f_buttons)
        f_buttons_layout.addLayout(fixed_buttons, 0, 0)

        # Layout para todos os botões
        buttons = HBoxLayout(0)
        buttons.addWidget(self.v_buttons)
        buttons.addStretch(1)
        buttons.addWidget(self.v_main)
        buttons.addWidget(f_buttons)

        # Ajustes do layout dos botões
        buttons_layout = GridLayout(None, 0)
        buttons_layout.addLayout(buttons, 0, 0)

        # Layout principal
        main_layout = QVBoxLayout(main_widget)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.stack)

        # Centralizar a janela
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    # Painel principal
    def get_main(self):
        self.stack.setCurrentIndex(0)
        self.v_buttons.setVisible(True)
        self.v_main.setVisible(False)

    # Painel sobre
    def get_about(self):
        self.stack.setCurrentIndex(1)
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)

    # Painel de configurações
    def get_settings(self):
        self.stack.setCurrentIndex(2)
        self.v_buttons.setVisible(False)
        self.v_main.setVisible(True)

    # Por enquanto vai servir
    def moveEvent(self, event):
        if not self.run_options.isHidden():
            self.run_options.set_resize(self.run.mapToGlobal(self.run.pos()))

    # Ação ao redirecionar a janela, o diágolo de opções pode variar de posição
    def resizeEvent(self, event):
        if not self.run_options.isHidden():
            self.run_options.set_resize(self.run.mapToGlobal(self.run.pos()))

    # Para fechar o diálogo ao clicar na interface
    def mouseReleaseEvent(self, event):
        if not self.run_options.isHidden():
            self.run_options.close()

    # Se tiver algo pendente, finalizar
    def closeEvent(self, event):
        self.run_options.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Theme.applyDarkMode()
    Translator.translate()

    sound_tagger = SoundTaggerApp()
    sound_tagger.show()
    sys.exit(app.exec_())
