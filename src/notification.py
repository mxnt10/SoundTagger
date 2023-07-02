import os

from plyer import notification


class Icons:
    @staticmethod
    def get(txt):
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


# Função básica para emitir notificações do programa
class Notification:
    @staticmethod
    def notify_send(app_title=str(), title=str(), message=str(), icon='info', timeout=5):
        name = 'Sound Tagger'
        if app_title != str():
            name += str(' - ' + app_title)

        notification.notify(
            app_name=name,
            app_icon=Icons.get(icon),
            title=title,
            message=message,
            timeout=timeout
        )
