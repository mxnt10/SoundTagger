import multiprocessing

from PyQt5.QtCore import Qt, QThreadPool, QItemSelection, QItemSelectionModel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction, QFileDialog, QHeaderView, QWidget, \
    QAbstractItemView, QCheckBox

from button import Button
from file_processor import FileProcessor
from list_delegate import ListDelegate
from list_enum import __CHECK__, __FILES__, __NUMS__, __BUTTONS__, __MESSAGES__
from music_utils import MusicUtils
from notification import Notification
from settings_manager import SettingsManager
from vboxlayout import VBoxLayout
from worker import Worker, SharedClass


# Classe que vai listar os arquivos multimídia
class ListWidget(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)  # 0 linhas e 5 colunas
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setColumnWidth(__CHECK__, 20)
        self.setColumnWidth(__NUMS__, 20)
        self.setColumnWidth(__BUTTONS__, 20)
        self.settings = SettingsManager()

        # Tornar colunas específicas expansíveis
        header = self.horizontalHeader()
        header.setSectionResizeMode(__FILES__, QHeaderView.Stretch)
        header.setSectionResizeMode(__MESSAGES__, QHeaderView.Stretch)

        # Estilização da lista
        self.setItemDelegate(ListDelegate())
        self.setStyleSheet('QTableWidget { border: none; background-color: transparent; }'
                           'QScrollBar { border: none; background-color: transparent; width: 10px; }'
                           'QScrollBar::handle { background-color: #9aa0a6; min-height: 10px; border-radius: 5px; }'
                           'QScrollBar::add-line, QScrollBar::sub-line { background: none; }'
                           'QScrollBar::add-page, QScrollBar::sub-page { background: none; }')

        self.current_item_index = None
        self.widget_event = None
        self.start_item = None
        self.end_item = None

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
                item = self.item(row, __FILES__)
                if item is not None and item.text() == file:
                    duplicate = True
                    continue

            if duplicate:
                continue  # Ignorar itens repetidos

            row_count = self.rowCount()
            self.insertRow(row_count)

            nm = QTableWidgetItem(str(row_count + 1) + '. ')
            nm.setTextAlignment(Qt.AlignCenter | Qt.AlignRight)
            rm_button = Button("remove-list", tooltip=self.tr('Remove File'), size=28)

            select_ck = QCheckBox()
            select_ck.setChecked(True)
            select_ck.stateChanged.connect(self.update_messages)

            w_ck = QWidget()
            w_ck.setStyleSheet('QWidget { border: 0; background-color: transparent; }')
            l_ck = VBoxLayout(parent=w_ck, margin=0, array_widgets=[select_ck])
            l_ck.setAlignment(Qt.AlignCenter | Qt.AlignRight)

            w_btn = QWidget()
            w_btn.setStyleSheet('QWidget { border: 0; background-color: transparent; }')
            l_btn = VBoxLayout(parent=w_btn, margin=0, array_widgets=[rm_button])
            l_btn.setAlignment(Qt.AlignCenter)

            self.setCellWidget(row_count, __CHECK__, w_ck)
            self.setItem(row_count, __NUMS__, nm)
            self.setItem(row_count, __FILES__, QTableWidgetItem(file))
            self.setItem(row_count, __MESSAGES__, QTableWidgetItem(self.tr('Selected for Search') + '!'))
            self.setCellWidget(row_count, __BUTTONS__, w_btn)

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
            nm = row + 1
            item = self.item(row, __NUMS__)
            item.setText(str(nm) + '. ')

    # Pegar os itens da lista e processar os arquivos de áudio
    def process_sounds(self):
        if int(self.rowCount()) == 0:
            return

        shared = None
        if self.settings.priority_api() == 'acoustID':
            comp = SharedClass()
            comp.emitting.connect(self.file_tagger)
            shared = comp

        self.check_and_stop_threadpool()

        # Multiprocessamento para processar a lista
        thread_pool = QThreadPool.globalInstance()
        thread_pool.setMaxThreadCount(multiprocessing.cpu_count())
        processor = FileProcessor()
        processor.return_json.connect(self.file_tagger)
        processor.return_process.connect(self.update_table)

        for row in range(self.rowCount()):

            if not self.cellWidget(row, __CHECK__).layout().itemAt(0).widget().isChecked():
                continue  # O checkbox não selecionado

            item = self.item(row, __FILES__)
            if item is not None:
                worker = Worker(processor, item.text(), row, shared_class=shared)
                thread_pool.start(worker)

    # Função para finalizar o processo conforme o resultado das requisições
    def file_tagger(self, result, row) -> None:
        print(result)
        if result.get('status') == 'success' and not result.get('result') is None:

            result_dict = result['result']
            normalized_keys = {key.lower(): value for key, value in result_dict.items()}

            artist = normalized_keys.get('artist')
            title = normalized_keys.get('title')
            album = normalized_keys.get('album')

            txt = str()
            if self.settings.load_int_convert_bool('file_addnum') is True:
                if row < 9: txt = '0'
                txt += str(row + 1)
                txt += ' - '

            text = str()
            if artist:
                text = str(artist)
            if title:
                if artist:
                    text += ' - '
                text += str(title)
            txt += text
            if album:
                if title or artist:
                    text += ' --- ' + self.tr('Album') + ': '
                text += str(album)

            self.update_table(self.tr('Found Music') + ' ( ' + text + ' )', row)

            file = self.item(row, __FILES__)
            if self.settings.load_int_convert_bool('file_tagger') is True:
                MusicUtils.apply_tags(file.text(), artist, title, album)

            if self.settings.load_int_convert_bool('rename_file') is True:
                rename = MusicUtils.rename_file(file.text(), txt)
                self.update_table(rename, row, __FILES__)

        else:
            self.update_table(self.tr('Music Not Found!'), row)
            if result.get('status') == 'error':
                error_dict = result['error']
                error = error_dict['error_message']
                code = error_dict['error_code']
                Notification().notify_send(app_title=self.tr('Error'),
                                           title=self.tr('Error Code') + ': ' + str(code),
                                           message=error,
                                           icon='error',
                                           timeout=10)

    # Atualizar informações da tabela
    def update_table(self, text, row, col=__MESSAGES__) -> None:
        item = self.item(row, col)
        item.setText(text)

    def update_messages(self, var) -> None:
        ck = self.sender()
        if ck:
            row = self.indexAt(ck.parent().pos()).row()
            if var == 2:
                self.update_table(self.tr(self.tr('Selected for Search') + '!'), row)
            else:
                self.update_table(self.tr(self.tr('Unselected File') + '!'), row)

    # Marca todos os checkbox da lista
    def select_all_ck(self) -> None:
        for row in range(self.rowCount()):
            self.cellWidget(row, __CHECK__).layout().itemAt(0).widget().setChecked(True)

    # Desmarca todos os checkbox da lista
    def unselect_all_ck(self) -> None:
        for row in range(self.rowCount()):
            self.cellWidget(row, __CHECK__).layout().itemAt(0).widget().setChecked(False)

    # Verificação para finalizar o processamento atual antes de iniciar outros processos
    @staticmethod
    def check_and_stop_threadpool() -> None:
        thread_pool = QThreadPool.globalInstance()
        if thread_pool.activeThreadCount() > 0:
            thread_pool.clear()

    # Widget para fechar ao pressionar a interface atual
    def setWidgetEvent(self, widget) -> None:
        self.widget_event = widget

    # Evento para gerar o menu de contexto para os arquivos na lista
    def contextMenuEvent(self, event):
        if self.rowCount() == 0:
            return

        menu = QMenu(self)
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == __FILES__:
            if len(self.selectedItems()) < 2:
                self.setCurrentCell(index.row(), index.column())
                self.current_item_index = index
                remove_current_action = QAction(self.tr('Remove Current Item'), self)
                remove_current_action.triggered.connect(self.remove_current_item_menu)
                menu.addAction(remove_current_action)
            else:
                remove_selected_action = QAction(self.tr('Remove Selected Items'), self)
                remove_selected_action.triggered.connect(self.remove_selected_items)
                menu.addAction(remove_selected_action)
        elif not index.isValid():
            self.clearSelection()

        select_all = QAction(self.tr('Select All to search'), self)
        select_all.triggered.connect(self.select_all_ck)
        menu.addAction(select_all)

        unselect_all = QAction(self.tr('Unselect All to search'), self)
        unselect_all.triggered.connect(self.unselect_all_ck)
        menu.addAction(unselect_all)

        menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                current_item = self.itemAt(event.pos())

                if current_item is not None:
                    self.end_item = current_item
                    selection_model = self.selectionModel()
                    selection_model.clearSelection()

                    try:
                        start_index = self.model().index(self.start_item.row(), __FILES__)
                        end_index = self.model().index(self.end_item.row(), __FILES__)
                        range_selection = QItemSelection(start_index, end_index)
                        selection_model.select(range_selection, QItemSelectionModel.Select)

                    except Exception as msg:
                        _ = msg  # Anulando a mensagem de erro que não precisa
                        pass
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                self.start_item = None
                self.end_item = None

        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()

        if not self.widget_event.isHidden():
            self.widget_event.close()
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                self.start_item = self.itemAt(event.pos())

                if self.start_item is not None:
                    self.clearSelection()
                    self.setCurrentCell(self.start_item.row(), __FILES__)
        super().mousePressEvent(event)
