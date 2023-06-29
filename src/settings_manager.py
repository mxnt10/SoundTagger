from PyQt5.QtCore import QSettings

from list_enum import __FALSE__


# Classe para gerenciar as configurações do programa
class SettingsManager:
    def __init__(self):
        self.settings = QSettings('SoundTagger', 'SoundTagger')

    # Salvar o valor da api audd
    def save_audd_api_key(self, api_key):
        self.settings.setValue('audD_API', api_key)
        self.settings.sync()

    # Carregar o valor da api audd
    def load_audd_api_key(self):
        return self.settings.value('audD_API', defaultValue=None)

    # Carregar configurações de valores numéricos
    def load_int_config(self, key, defaultValue=__FALSE__):
        return int(self.settings.value(key, defaultValue=defaultValue))

    # Salvar configurações de valores numéricos
    def save_int_config(self, key, val) -> None:
        self.settings.setValue(key, val)
        self.settings.sync()
