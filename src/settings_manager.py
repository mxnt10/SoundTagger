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
