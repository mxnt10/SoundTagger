import sys

from PyQt5.QtGui import QMouseEvent, QCloseEvent, QContextMenuEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QStackedWidget, QSplitter, QMenu, \
    QAction

from about import About
from background import Background
from controls import Controls
from edit_tools import editTools
from gridlayout import GridLayout
from hboxlayout import HBoxLayout
from icon import IconPrg
from list import ListWidget
from list_enum import __FILES__
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
        self.setMinimumSize(800, 420)
        self.setStyleSheet(Background().get_background())

        # Widget da interface principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Resolvi centralizar as notificações
        self.notify = Notification()

        # Definição da lista
        self.run_options = RunOptions(self)
        self.list_widget = ListWidget()
        self.list_widget.set_notificator(self.notify)
        self.list_widget.set_widget_event(self.run_options)
        self.list_widget.added.connect(lambda: self.buttons.active_buttons())
        self.list_widget.removed.connect(lambda: self.buttons.deactive_buttons())
        self.list_widget.show_tag.connect(self.active_tags)
        self.list_widget.clean_selection.connect(self.deactive_tags)
        self.run_options.run.connect(self.list_widget.process_sounds)

        # Definição do editor de tag
        self.edit_tools = editTools()

        # Widget da lista para o splitter
        table = QWidget()
        layout_list = GridLayout(parent=table, margin=0)
        layout_list.addLayout(HBoxLayout(margin=10, array_widgets=[self.list_widget]), 0, 0)

        # Widget do editor de tag para o splitter
        self.tagedit = QWidget()
        self.tagedit.setVisible(False)
        layout_tag = GridLayout(parent=self.tagedit, margin=0)
        layout_tag.addLayout(HBoxLayout(margin=10, array_widgets=[self.edit_tools]), 0, 0)

        # Splitter para o QStackedWidget
        splitter = QSplitter()
        splitter.addWidget(table)
        splitter.addWidget(self.tagedit)
        splitter.setSizes([table.width() - 300, 300])
        splitter.setHandleWidth(5)

        # Lista de widgets para sobreposição
        self.stack = QStackedWidget()
        self.stack.addWidget(splitter)
        self.stack.addWidget(About())
        self.stack.addWidget(Settings())

        # Controles principais
        self.buttons = Controls()
        self.buttons.control_add.connect(self.list_widget.add_item)
        self.buttons.control_remove.connect(self.list_widget.remove_selected_items)
        self.buttons.control_clean.connect(self.list_widget.clear_items)
        self.buttons.control_point.connect(self.run_options.set_point)
        self.buttons.control_options.connect(self.show_options)
        self.buttons.control_main.connect(lambda: self.change_stack(0))
        self.buttons.control_settings.connect(lambda: self.change_stack(2))
        self.buttons.control_about.connect(lambda: self.change_stack(1))

        # Layout principal
        main_layout = VBoxLayout(parent=main_widget)
        main_layout.addLayout(GridLayout(margin=0, layout=self.buttons))
        main_layout.addWidget(self.stack)

        # Centralizar a janela
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

        # Resolvendo um probleminha, run_options não está vinculado a nenhum widget, então ele abre
        self.run_options.close()

########################################################################################################################

    # Função para abrir opções antes de iniciar a operação
    def show_options(self) -> None:
        s = SettingsManager()
        if s.priority_api() is not None:
            self.run_options.show()
            self.list_widget.clearSelection()
            self.tagedit.setVisible(False)

        else:
            self.notify.notify_send(app_title=self.tr('Information'),
                                    title=self.tr('Configure an API Key'),
                                    message=self.tr('No API Key has been configured!'),
                                    icon='key')

    # Ativar edição de tags
    def active_tags(self, n) -> None:
        self.edit_tools.set_file(self.list_widget.item(n, __FILES__).text())
        if self.tagedit.isHidden():
            if self.edit_tools.is_file_supported():
                self.tagedit.setVisible(True)
            else:
                self.tagedit.setVisible(False)

    # Destivar edição de tags
    def deactive_tags(self) -> None:
        if self.run_options.isHidden():
            self.tagedit.setVisible(False)

    # Função pra alterar as interfaces do programa
    def change_stack(self, n) -> None:
        if n > 0:
            if not self.run_options.isHidden():
                self.run_options.close()
        self.stack.setCurrentIndex(n)

########################################################################################################################

    # Para fechar o diálogo ao clicar na interface
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if not self.run_options.isHidden():
            self.run_options.close()
        super().mouseReleaseEvent(event)

    # Se tiver algo pendente, finalizar
    def closeEvent(self, event: QCloseEvent) -> None:
        self.run_options.close()
        event.accept()

    # Menu de contexto de escopo global
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)

        add = QAction(self.tr('Add Files'), self)
        add.triggered.connect(self.list_widget.add_item)
        menu.addAction(add)

        menu.exec_(event.globalPos())

########################################################################################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)

    t = Theme()
    t.viewColors()
    t.applyAutoMode()

    Translator().translate()

    sound_tagger = SoundTaggerApp()
    sound_tagger.show()
    sys.exit(app.exec_())
