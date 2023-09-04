import os

from PyQt5.QtCore import QObject

from plyer import notification


# Função básica para emitir notificações do programa
class Notification(QObject):
    def __init__(self):
        super().__init__()
        self.nm = 0

    # Função para achar os ícones das notificações
    @staticmethod
    def get_icons(txt):
        def_icon = "/usr/share/SoundTagger/notification"
        rel_icon = os.path.abspath("../notification")
        alt_icon = os.path.abspath("notification")

        if os.path.exists(def_icon + '/' + txt + '.png'):
            return def_icon + '/' + txt + '.png'
        if os.path.exists(rel_icon + '/' + txt + '.png'):
            return rel_icon + '/' + txt + '.png'
        if os.path.exists(alt_icon + '/' + txt + '.png'):
            return alt_icon + '/' + txt + '.png'
        return str()

    # Função para as notificações
    def notify_send(self, app_title=str(), title=str(), message=str(), icon='info', timeout=5):

        self.nm += 1
        print(f'(\033[92mnotification\033[m) notify count: {self.nm}')

        name = str('Sound Tagger - ' + app_title) if app_title != str() else 'Sound Tagger'

        try:
            notification.notify(
                app_name=name,
                app_icon=self.get_icons(icon),
                title=title,
                message=message,
                timeout=timeout
            )
        except Exception as msg:
            print(f'\033[91m{type(msg)}\033[m')
            print(f'(\033[92mfile_processor\033[m) {msg}')
            pass  # aqui eu uso o pass
