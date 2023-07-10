import os

from plyer import notification


# Função básica para emitir notificações do programa
class Notification:

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
        name = 'Sound Tagger'
        if app_title != str():
            name += str(' - ' + app_title)

        notification.notify(
            app_name=name,
            app_icon=self.get_icons(icon),
            title=title,
            message=message,
            timeout=timeout
        )
