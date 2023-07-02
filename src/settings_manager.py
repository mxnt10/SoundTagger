from PyQt5.QtCore import QSettings

from list_enum import __FALSE__


# Classe para gerenciar as configurações do programa
class SettingsManager:
    def __init__(self):
        self.settings = QSettings('SoundTagger', 'SoundTagger')

    # Função para definir a api prioritária
    def priority_api(self):
        for api in self.load_priorities_API().split(':'):
            if self.load_api_key(api + '_API') != str():
                return api
        return None

    # Salvar o valor da api audd
    def save_api_key(self, key, api_key):
        self.settings.setValue(key, api_key)
        self.settings.sync()

    # Carregar o valor da api audd
    def load_api_key(self, key):
        return self.settings.value(key, defaultValue=str())

    # Carregar configurações de valores numéricos
    def load_int_config(self, key, defaultValue=__FALSE__):
        return int(self.settings.value(key, defaultValue=defaultValue))

    # Salvar configurações de valores numéricos
    def save_int_config(self, key, val) -> None:
        self.settings.setValue(key, val)
        self.settings.sync()

    # Carregar lista de prioridade das APIs
    def load_priorities_API(self):
        return self.settings.value('Priorities_API', defaultValue='acoustID:audD')

    # Salvar lista de prioridades das APIs
    def save_priorities_API(self, val):
        self.settings.setValue('Priorities_API', val)
        self.settings.sync()
