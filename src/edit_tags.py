from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from form import Form
from hboxlayout import HBoxLayout
from mutagen_utils import MU
from scrool_area import ScrollArea
from vboxlayout import VBoxLayout


########################################################################################################################


# A classe para edição das tags
class editTags(QWidget):
    visible = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.support = False
        self.m = MU()

        artist = Form(self.tr('Artist'))
        title = Form(self.tr('Title'))
        album = Form(self.tr('Album'))
        album_artist = Form(self.tr('Album Artist'))
        genre = Form(self.tr('Genre'))
        date = Form(self.tr('Date'))
        first_track = Form(self.tr('Track'), orig=True)
        end_track = Form('/', orig=True, d='', space=7)
        composer = Form(self.tr('Composer'))
        copy = Form(self.tr('Copyright'))
        encoded = Form(self.tr('Encoded by'))
        self.language = Form(self.tr('Language'))
        self.orig_artist = Form(self.tr('Original Artist'))
        comments = Form(self.tr('Comments'), form='text')
        url = Form(self.tr('Url'))
        cd = Form(self.tr('Disc Number'), orig=True)

        self.general = (
            [artist, 'artist'],
            [artist, 'performer'],
            [title, 'title'],
            [album, 'album'],
            [cd, 'discnumber'],
            [album_artist, 'albumartist'],
            [genre, 'genre'],
            [date, 'date'],
            [first_track, 'tracknumber'],
            [end_track, 'tracknumber'],
            [end_track, 'tracktotal'],
            [composer, 'composer'],
            [copy, 'copyright'],
            [encoded, 'encodedby'],
            [encoded, 'encoded-by'],
            [encoded, 'encoded_by'],
            [self.orig_artist, 'originalartist'],
            [self.orig_artist, 'tope'],
            [comments, 'comment'],
            [self.language, 'language'],
            [url, 'website'],
            [url, 'contact']
        )

        self.mp3Tag = (
            [copy, 'TCOP'],                  # copyright
            [title, 'TIT2'],                 # título
            [artist, 'TPE1'],                # artista
            [album, 'TALB'],                 # album
            [date, 'TDRC'],                  # date
            [first_track, 'TRCK'],           # track
            [end_track, 'TRCK'],             # track
            [end_track, 'TXXX:TRACKTOTAL'],  # track
            [genre, 'TCON'],                 # genero
            [album_artist, 'TPE2'],          # album artist
            [url, 'WOAR'],                   # site
            [url, 'WXXX'],                   # MP3
            [comments, 'COMM'],              # comentário
            [self.orig_artist, 'TOPE'],      # original artist
            [self.language, 'TLAN'],         # idioma
            [cd, 'TPOS'],                    # disco
            [encoded, 'TENC'],               # encoded by
            [composer, 'TCOM']               # compositor
        )

        self.mp4tag = (
            [artist, '©ART'],        # artist
            [title, '©nam'],         # title
            [album, '©alb'],         # album
            [album_artist, 'aART'],  # album artist
            [genre, '©gen'],         # genero
            [date, '©day'],          # ano
            [composer, '©wrt'],      # composer
            [copy, 'cprt'],          # copyright
            [first_track, 'trkn'],   # track
            [end_track, 'trkn'],     # track
            [comments, '©cmt'],      # comentario
            [encoded, '©enc'],       # encoded by
            [cd, 'disk'],            # disk number
            [url, 'purl']            # url
        )

        self.apeTag = (
            [artist, 'Artist'],
            [title, 'Title'],
            [album, 'Album'],
            [album_artist, 'Album Artist'],
            [first_track, 'Track'],
            [end_track, 'Track'],
            [composer, 'Composer'],
            [genre, 'Genre'],
            [self.orig_artist, 'Original Artist'],
            [date, 'Year'],
            [cd, 'Part'],
            [self.language, 'Language'],
            [url, 'Related'],
            [copy, 'Copyright'],
            [encoded, 'Encoded By'],
            [comments, 'Comment']
        )

        self.asfTag = (
            [artist, 'Author'],
            [title, 'Title'],
            [album, 'WM/AlbumTitle'],
            [album_artist, 'WM/AlbumArtist'],
            [first_track, 'WM/TrackNumber'],
            [end_track, 'WM/TrackNumber'],
            [composer, 'WM/Composer'],
            [genre, 'WM/Genre'],
            [self.orig_artist, 'WM/OriginalArtist'],
            [date, 'WM/Year'],
            [cd, 'WM/PartOfSet'],
            [self.language, 'WM/Language'],
            [url, 'WM/AuthorURL'],
            [copy, 'Copyright'],
            [encoded, 'WM/EncodedBy'],
            [comments, 'Description']
        )

        self.mpcTag = (
            [artist, 'ARTIST'],
            [title, 'TITLE'],
            [album, 'ALBUM'],
            [album_artist, 'ALBUMARTIST'],
            [first_track, 'TRACK'],
            [end_track, 'TRACK'],
            [end_track, 'TRACKTOTAL'],
            [composer, 'COMPOSER'],
            [genre, 'GENRE'],
            [self.orig_artist, 'ORIGINALARTIST'],
            [date, 'YEAR'],
            [cd, 'DISCNUMBER'],  # DISCTOTAL
            [self.language, 'LANGUAGE'],
            [url, 'WEBSITE'],
            [copy, 'COPYRIGHT'],
            [encoded, 'ENCODED-BY'],
            [comments, 'COMMENT']
        )

        lay_cd = HBoxLayout(margin=0, space=0, array_widgets=[album, cd])
        lay_track = HBoxLayout(margin=0, space=0, array_widgets=[date, first_track, end_track])

        scroll_widget = QWidget()
        VBoxLayout(parent=scroll_widget,
                   array_widgets=[artist, title, lay_cd, album_artist, genre, lay_track, composer,
                                  self.orig_artist, copy, self.language, encoded, url, comments])

        scroll_area = ScrollArea()
        scroll_area.setWidget(scroll_widget)

        main_layout = VBoxLayout(spacing=2)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # Vai ser usado para pescar as informações para gerar uma dict
        self.order = [
            artist, title, album, cd, album_artist, genre, date, first_track, end_track, composer,
            self.orig_artist, copy, self.language, encoded, url, comments
        ]

        # Executando uma ação ao alterar uma informação
        for form in self.order:
            form.changeText.connect(self.form_actions)

########################################################################################################################

    # Setando o arquivo para a leitura das tags
    def set_file(self, file) -> None:
        self.support = False

        # Redefinindo os campos
        for tag in self.general:
            tag[0].setText('')
            tag[0].clearFocus()
        self.orig_artist.setEnabled(True)
        self.language.setEnabled(True)

        mime = self.m.is_supported(file)
        if mime is not None:
            if self.m.regex(mime, r'aiff|mp3|trueaudio|wave'):
                self.m.get_tags(mime, file, self.mp3Tag)
            elif mime == 'mp4':
                self.orig_artist.setEnabled(False)
                self.language.setEnabled(False)
                self.m.get_tags(mime, file, self.mp4tag)
            elif self.m.regex(mime, r'monkeysaudio|wavpack'):
                self.m.get_tags(mime, file, self.apeTag)
            elif mime == 'asf':
                self.m.get_tags(mime, file, self.asfTag)
            elif mime == 'musepack':
                self.m.get_tags(mime, file, self.mpcTag)
            else:
                self.m.get_tags(mime, file, self.general)

            self.support = True

    # Verificando se o arquivo é suportado pelo mutagen
    def is_file_supported(self):
        return self.support

    # Gerar um arquivo de dicionário pra compatibilizar com a função para gravar as id tags nos arquivos de mídia
    def generate_dict(self):
        obj = {}
        i = 0
        for form in self.order:
            obj[self.m.order_tags()[i]] = str(form.text())
            i += 1
        return obj

    # Gravando as id tags nos arquivos de mídia
    def apply_tags(self, file) -> None:
        self.m.apply_tags(mime=self.m.is_supported(file), file=file, keys=self.generate_dict())

    # Ação após editar algum campo do formulário das tags
    def form_actions(self, txt):
        _ = txt
        if not self.support:
            return
        self.visible.emit()
