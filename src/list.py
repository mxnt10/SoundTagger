import multiprocessing

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction, QFileDialog, QHeaderView, QWidget, \
    QVBoxLayout, QAbstractItemView

from button import Button
from file_processor import FileProcessor, Worker
from list_delegate import ListDelegate
from music_tagger import MusicTagger
from settings_manager import SettingsManager


# Classe que vai listar os arquivos multimídia
class ListWidget(QTableWidget):
    def __init__(self):
        super().__init__(0, 4)  # 0 linhas e 4 colunas
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setColumnWidth(0, 25)
        self.setColumnWidth(3, 40)
        self.settings = SettingsManager()

        # Tornar colunas específicas expansíveis
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # Estilização da lista
        self.setItemDelegate(ListDelegate())
        self.setStyleSheet('QTableWidget { border: none; background-color: transparent; }'
                           'QScrollBar { border: none; background-color: transparent; width: 12px; }'
                           'QScrollBar::handle { background-color: #777; min-height: 12px; border-radius: 6px; }'
                           'QScrollBar::add-line, QScrollBar::sub-line { background: none; }'
                           'QScrollBar::add-page, QScrollBar::sub-page { background: none; }')

        self.current_item_index = None  # Índice do item atualmente selecionado
        self.widget_event = None

    # Adicionar os arquivos de áudio na lista
    def add_item(self):
        file_dialog = QFileDialog()
        files, _ = file_dialog.getOpenFileNames(None, 'Selecionar Arquivos', '',
                                                'Todos os Arquivos (*);;Music Files (*.mp3 *.wma *.m4a)')

        if not files:
            return  # Retorna se a lista de arquivos está vazia

        for file in files:
            duplicate = False

            # Verificar duplicatas na segunda coluna, porque a primeira é os números
            for row in range(self.rowCount()):
                item = self.item(row, 1)
                if item is not None and item.text() == file:
                    duplicate = True
                    continue

            if duplicate:
                continue  # Ignorar itens repetidos

            row_count = self.rowCount()
            self.insertRow(row_count)

            nm = QTableWidgetItem(str(self.rowCount()))
            nm.setTextAlignment(Qt.AlignCenter)
            rm_button = Button("remove-list", self.tr('Remove File'), 28)

            w_btn = QWidget()
            w_btn.setStyleSheet('border: 0; background-color: transparent;')
            l_btn = QVBoxLayout(w_btn)
            l_btn.setContentsMargins(0, 0, 0, 0)
            l_btn.addWidget(rm_button)
            l_btn.setAlignment(Qt.AlignCenter)

            self.setItem(row_count, 0, nm)
            self.setItem(row_count, 1, QTableWidgetItem(file))
            self.setItem(row_count, 2, QTableWidgetItem('Pendente'))
            self.setCellWidget(row_count, 3, w_btn)

            rm_button.clicked.connect(self.remove_current_item)

    # Remover arquivo atualmente selecionado com o botão
    def remove_current_item(self) -> None:
        button = self.sender()
        if button:
            row = self.indexAt(button.parent().pos()).row()
            if row != -1:
                self.removeRow(row)
                self.update_item_numbers()

    # Remover arquivo atualmente selecionado no menu
    def remove_current_item_menu(self) -> None:
        if self.current_item_index is not None:
            row = self.current_item_index.row()
            if row != -1:
                self.removeRow(row)
                self.update_item_numbers()

    # Removes vários arquivos selecionados
    def remove_selected_items(self) -> None:
        selected_rows = set()
        for item in self.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            self.removeRow(row)
            self.update_item_numbers()

    # Limpar a lista
    def clear_items(self) -> None:
        self.setRowCount(0)

    # Atualizar numeração dos itens da lista
    def update_item_numbers(self) -> None:
        for row in range(self.rowCount()):
            item_number = row + 1
            item = self.item(row, 0)
            item.setText(str(item_number))

    # Pegar os itens da lista e processar os arquivos de áudio
    def process_sounds(self):
        if int(self.rowCount()) == 0:
            return

        sett = self.settings.load_audd_api_key()
        if sett is None or sett == '':
            return

        self.check_and_stop_threadpool()

        # Multiprocessamento para processar a lista
        thread_pool = QThreadPool.globalInstance()
        thread_pool.setMaxThreadCount(multiprocessing.cpu_count())
        processor = FileProcessor()
        processor.return_json.connect(self.file_tagger)
        processor.return_process.connect(self.update_table)

        for row in range(self.rowCount()):
            item = self.item(row, 1)
            if item is not None:
                self.update_table(self.tr('Start') + '...', row)

                worker = Worker(processor, item.text(), row)
                thread_pool.start(worker)

    # Função para finalizar o processo conforme o resultado das requisições
    def file_tagger(self, result, row):
        self.update_table(self.tr('Search Finished') + '!', row)

        if result.get('status') == 'success' and not result.get('result') is None:

            result_dict = result['result']
            normalized_keys = {key.lower(): value for key, value in result_dict.items()}

            artist = normalized_keys.get('artist')
            title = normalized_keys.get('title')
            album = normalized_keys.get('album')

            text = ''
            if artist:
                text = str(artist)
            if title:
                if artist:
                    text += ' - '
                text += str(title)
            txt = text
            if album:
                if title or artist:
                    text += ' --- ' + self.tr('Album') + ': '
                text += str(album)

            self.update_table(self.tr('Found Music') + ' ( ' + text + ' )', row)

            if self.settings.load_rename_file() == 2:
                file = self.item(row, 1)
                rename = MusicTagger.rename_file(file.text(), txt)
                self.update_table(rename, row, 1)

            if self.settings.load_file_tagger() == 2:
                file = self.item(row, 1)
                MusicTagger.apply_tags(file.text(), artist, title, album)

        else:
            self.update_table(self.tr('Music Not Found!'), row)

    # Atualizar informações da tabela
    def update_table(self, text, row, col=2):
        item = self.item(row, col)
        item.setText(text)

    # Verificação para finalizar o processamento atual antes de iniciar outros processos
    @staticmethod
    def check_and_stop_threadpool():
        thread_pool = QThreadPool.globalInstance()
        if thread_pool.activeThreadCount() > 0:
            thread_pool.clear()

    # Widget para fechar ao pressionar a interface atual
    def setWidgetEvent(self, widget):
        self.widget_event = widget

    # Evento para gerar o menu de contexto para os arquivos na lista
    def contextMenuEvent(self, event):

        if self.rowCount() == 0:
            return

        menu = QMenu(self)
        remove_selected_action = QAction('Remove Selected Items', self)
        remove_selected_action.triggered.connect(self.remove_selected_items)

        index = self.indexAt(event.pos())
        if index.isValid():
            self.current_item_index = index
            remove_current_action = QAction('Remove Current Item', self)
            remove_current_action.triggered.connect(self.remove_current_item_menu)
            menu.addAction(remove_current_action)

        menu.addAction(remove_selected_action)
        menu.exec_(event.globalPos())

    # Evento para fechar o widget selecionado ao pressionar a interface principal
    def mouseReleaseEvent(self, event):
        if not self.widget_event.isHidden():
            self.widget_event.close()
