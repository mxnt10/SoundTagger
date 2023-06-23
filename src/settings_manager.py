from PyQt5.QtCore import QSettings


# Classe para gerenciar as configurações do programa
class SettingsManager:
    def __init__(self):
        self.settings = QSettings('MusicTagger', 'MusicTagger')

    # Salvar o valor da api audd
    def save_audd_api_key(self, api_key):
        self.settings.setValue('audD_API', api_key)
        self.settings.sync()

    # Carregar o valor da api audd
    def load_audd_api_key(self):
        return self.settings.value('audD_API', defaultValue=None)

    # Salvar a configuração para renomear arquivos
    def save_rename_file(self, val):
        self.settings.setValue('rename_file', val)
        self.settings.sync()

    # Carregar a configuração para renomear arquivos
    def load_rename_file(self):
        return self.settings.value('rename_file', defaultValue='0')

    # Salvar a configuração para taggear arquivos
    def save_file_tagger(self, val):
        self.settings.setValue('file_tagger', val)
        self.settings.sync()

    # Carregar a configuração para taggear arquivos
    def load_file_tagger(self):
        return self.settings.value('file_tagger', defaultValue='0')
