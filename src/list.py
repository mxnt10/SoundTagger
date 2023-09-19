import multiprocessing

from PyQt5.QtCore import Qt, QThreadPool, QItemSelection, QItemSelectionModel, pyqtSignal, QRect
from PyQt5.QtGui import QMouseEvent, QPainter, QBrush, QPalette, QPaintEvent, QContextMenuEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction, QFileDialog, QHeaderView, QWidget, \
    QAbstractItemView

from button import Button
from checkbox import CheckBox
from file_processor import FileProcessor
from list_delegate import ListDelegate
from list_enum import __CHECK__, __FILES__, __NUMS__, __BUTTONS__, __MESSAGES__
from settings_manager import SettingsManager
from rename_utils import RenameUtils
from mutagen_utils import MU
from theme import Theme
from vboxlayout import VBoxLayout
from worker import Worker, SharedClass


########################################################################################################################


# Classe que vai listar os arquivos multimídia
class ListWidget(QTableWidget):
    added = pyqtSignal()
    removed = pyqtSignal()
    show_tag = pyqtSignal(int)
    clean_selection = pyqtSignal()

    def __init__(self):
        super().__init__(0, 5)  # 0 linhas e 5 colunas
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
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
        self.t = Theme()
        self.setItemDelegate(ListDelegate(self))
        self.setStyleSheet(
            f'QTableWidget {{'
            f'    border: none;'
            f'    background-color: transparent;'
            f'}}'
            f'QScrollBar {{'
            f'    border: none;'
            f'    background-color: transparent;'
            f'    width: 10px;'
            f'}}'
            f'QScrollBar::handle {{'
            f'    background-color: {self.t.color_palette(QPalette.Light)};'
            f'    min-height: 10px;'
            f'    border-radius: 5px;'
            f'    border: 2px solid transparent;'
            f'}}'
            f'QScrollBar::add-line, QScrollBar::sub-line {{'
            f'    background: none;'
            f'}}'
            f'QScrollBar::add-page, QScrollBar::sub-page {{'
            f'    background: none;'
            f'}}'
        )

        self.current_item_index = None
        self.widget_event = None
        self.start_item = None
        self.end_item = None
        self.current_item = None
        self.notify = None

        self.itemSelectionChanged.connect(self.on_selection_changed)

########################################################################################################################

    # Setando a função de notificações
    def set_notificator(self, notificator) -> None:
        self.notify = notificator

    # Ação ao selecionar qualquer item da lista
    def on_selection_changed(self):
        if self.rowCount() == 0:
            return

        selected_items = self.selectedItems()
        if selected_items:
            self.current_item = selected_items

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
            rm_button = Button("remove-list", tooltip=self.tr('Remove File'), size=31, click=0)

            select_ck = CheckBox(checked=True)
            select_ck.stateChanged.connect(self.update_messages)

            w_ck = QWidget()
            w_ck.setStyleSheet('QWidget { border: 0; background-color: transparent; }')
            l_ck = VBoxLayout(parent=w_ck, margin=0, array_widgets=[select_ck])
            l_ck.setAlignment(Qt.AlignCenter | Qt.AlignRight)

            w_btn = QWidget()
            w_btn.setStyleSheet('QWidget { border: 0; background-color: transparent; }')
            l_btn = VBoxLayout(parent=w_btn, margin=0, array_widgets=[rm_button])
            l_btn.setAlignment(Qt.AlignCenter | Qt.AlignLeft)

            self.setCellWidget(row_count, __CHECK__, w_ck)
            self.setItem(row_count, __NUMS__, nm)
            self.setItem(row_count, __FILES__, QTableWidgetItem(file))
            self.setItem(row_count, __MESSAGES__, QTableWidgetItem(f'{self.tr("Selected for Search")}!'))
            self.setCellWidget(row_count, __BUTTONS__, w_btn)

            rm_button.clicked.connect(self.remove_current_item)
        self.added.emit()

    # Remover arquivo atualmente selecionado com o botão
    def remove_current_item(self) -> None:
        button = self.sender()
        if button:
            row = self.indexAt(button.parent().pos()).row()
            if row != -1:
                self.removeRow(row)
                self.update_item_numbers()

            if int(self.rowCount()) == 0:
                self.removed.emit()
                self.clean_selection.emit()

    # Remover arquivo atualmente selecionado no menu
    def remove_current_item_menu(self) -> None:
        if self.current_item_index is not None:
            row = self.current_item_index.row()
            if row != -1:
                self.removeRow(row)
                self.update_item_numbers()

            if int(self.rowCount()) == 0:
                self.removed.emit()
                self.clean_selection.emit()

    # Removes vários arquivos selecionados
    def remove_selected_items(self) -> None:
        selected_rows = set()
        for item in self.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            self.removeRow(row)
            self.update_item_numbers()

        if int(self.rowCount()) == 0:
            self.removed.emit()
            self.clean_selection.emit()

    # Limpar a lista
    def clear_items(self) -> None:
        self.setRowCount(0)
        self.clean_selection.emit()
        self.removed.emit()

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
                worker = Worker(processor, item.text(), row, shared_class=shared, notificator=self.notify)
                thread_pool.start(worker)

    # Função para finalizar o processo conforme o resultado das requisições
    def file_tagger(self, result, row) -> None:
        print(f'(\033[92mlist\033[m) {result}')
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
                    text += f' --- {self.tr("Album")}: '
                text += str(album)

            self.update_table(f'{self.tr("Found Music")} ( {text} )', row)

            file = self.item(row, __FILES__).text()
            if self.settings.load_int_convert_bool('file_tagger') is True:
                mu = MU()
                mime = mu.isSupported(file)
                if mime is not None:
                    mu.applyTags(mime=mime, file=file, keys=normalized_keys)

            if self.settings.load_int_convert_bool('rename_file') is True:
                rename = RenameUtils.rename_file(file, txt)
                self.update_table(rename, row, __FILES__)

        else:
            self.update_table(self.tr('Music Not Found!'), row)
            if result.get('status') == 'error':
                error_dict = result['error']
                error = error_dict['error_message']
                code = error_dict['error_code']
                self.notify.notify_send(app_title=self.tr('Error'),
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
                self.update_table(f'{self.tr("Selected for Search")}!', row)
            else:
                self.update_table(f'{self.tr("Unselected File")}!', row)

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

    def index_row(self):
        try:
            return int(self.row(self.selectedItems()[0]))
        except Exception as msg:
            _ = msg
            return -1

########################################################################################################################

    # Evento para gerar o menu de contexto para os arquivos na lista
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)

        add = QAction(self.tr('Add Files'), self)
        add.triggered.connect(self.add_item)
        menu.addAction(add)

        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == __FILES__:
            if len(self.selectedItems()) < 2 * 3:  # Sério
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
            self.clean_selection.emit()

        if self.rowCount() > 0:
            select_all = QAction(self.tr('Select All to search'), self)
            select_all.triggered.connect(self.select_all_ck)
            menu.addAction(select_all)

            unselect_all = QAction(self.tr('Unselect All to search'), self)
            unselect_all.triggered.connect(self.unselect_all_ck)
            menu.addAction(unselect_all)

        menu.exec_(event.globalPos())

    # Ação ao mover o mouse após pressionado
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                current_item = self.itemAt(event.pos())

                if current_item is not None:
                    self.end_item = current_item
                    selection_model = self.selectionModel()
                    selection_model.clearSelection()

                    try:  # Só por precaução
                        start_index = self.model().index(self.start_item.row(), __FILES__)
                        end_index = self.model().index(self.end_item.row(), __FILES__)
                        range_selection = QItemSelection(start_index, end_index)
                        selection_model.select(range_selection, QItemSelectionModel.Select)

                    except Exception as msg:
                        _ = msg  # Anulando a mensagem de erro que não precisa
                        pass
        super().mouseMoveEvent(event)

    # Ação ao despressionar o mouse
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()
            self.clean_selection.emit()

        # Emissão do item atual selecionado
        if self.current_item is not None and (self.end_item is None or self.start_item == self.end_item):
            try:  # Sem bestera
                self.show_tag.emit(self.current_item[0].row())
            except Exception as msg:
                _ = msg  # Convenção do _
                pass
        self.current_item = None

        if event.button() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                self.start_item = None
                self.end_item = None

        # Fechar run_options
        if not self.widget_event.isHidden():
            self.widget_event.close()
        super().mouseReleaseEvent(event)

    # Ação ao pressionar o mouse
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.selectionMode() == QAbstractItemView.ExtendedSelection:
                self.start_item = self.itemAt(event.pos())

                if self.start_item is not None:
                    self.clearSelection()
                    self.setCurrentCell(self.start_item.row(), __FILES__)
        super().mousePressEvent(event)

    # Função para pintar a linha selecionada
    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)
        selected_rows = self.selectionModel().selectedRows()

        for index in selected_rows:
            option = self.viewOptions()
            option.rect = self.visualRect(index)

            highlight_color = QPalette().color(QPalette.Highlight)
            highlight_color.setAlpha(self.t.__SELECT__)

            painter.save()
            painter.setBrush(QBrush(highlight_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRect(0, option.rect.top(), self.width() - 10, option.rect.height()), 16, 16)
            painter.restore()
