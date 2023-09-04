from PyQt5.QtWidgets import QWidget

from form import Form
from hboxlayout import HBoxLayout
from mutagen_utils import MU
from scrool_area import ScrollArea
from vboxlayout import VBoxLayout

########################################################################################################################


# A classe para edição das tags
class editTags(QWidget):
    def __init__(self):
        super().__init__()
        self.media = None
        self.support = False

        artist = Form(self.tr('Artist'))
        title = Form(self.tr('Title'))
        album = Form(self.tr('Album'))
        album_artist = Form(self.tr('Album Artist'))
        genre = Form(self.tr('Genre'))
        date = Form(self.tr('Date'))
        first_track = Form(self.tr('Track'), orig=True)
        end_track = Form('/', orig=True, d=str(), space=7)
        composer = Form(self.tr('Composer'))
        copy = Form(self.tr('Copyright'))
        encoded = Form(self.tr('Encoded by'))
        self.language = Form(self.tr('Language'))
        self.orig_artist = Form(self.tr('Original Artist'))
        comments = Form(self.tr('Comments'), form='text')
        url = Form(self.tr('Url'))
        cd = Form(self.tr('Disc Number'), orig=True)

        self.general = (
            [artist, 'artist'],               #
            [title, 'title'],                 #
            [album, 'album'],                 #
            [cd, 'discnumber'],               # by easyTag
            [cd, 'part'],                     # wavpack
            [album_artist, 'albumartist'],    #
            [album_artist, 'album_artist'],   # wavpack
            [album_artist, 'album artist'],   # wavpack
            [genre, 'genre'],                 #
            [date, 'date'],                   #
            [date, 'year'],                   # wavpack
            [first_track, 'tracknumber'],     #
            [first_track, 'track'],           # wavpack
            [end_track, 'tracknumber'],       #
            [end_track, 'track'],             # wavpack
            [end_track, 'tracktotal'],        #
            [composer, 'composer'],           #
            [copy, 'copyright'],              #
            [encoded, 'encodedby'],           #
            [encoded, 'encoded_by'],          # wavpack
            [encoded, 'encoded-by'],          # flac
            [self.orig_artist, 'tope'],       # COMPATIBILIDADE
            [self.orig_artist, 'performer'],  # flac
            [comments, 'comment'],            #
            [comments, 'description'],        # flac
            [self.language, 'language'],      #
            [url, 'contact'],                 # flac
            [url, 'website']                  # opus
        )

        self.aiffTag = (
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
            [album, 'AlbumTitle'],
            [album_artist, 'AlbumArtist'],
            [first_track, 'TrackNumber'],
            [end_track, 'TrackNumber'],
            [composer, 'Composer'],
            [genre, 'Genre'],
            [self.orig_artist, 'OriginalArtist'],
            [date, 'Year'],
            [cd, 'PartOfSet'],
            [self.language, 'Language'],
            [url, 'AuthorURL'],
            [copy, 'Copyright'],
            [encoded, 'EncodedBy'],
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

    # Setando o arquivo para a leitura das tags
    def setFile(self, file) -> None:
        for tag in self.general:
            tag[0].setText(str())
        self.orig_artist.setEnabled(True)
        self.language.setEnabled(True)

        self.support = False
        mu = MU()
        mime = mu.isSupported(file)

        if mime is not None:
            if mu.equal(mime, ['aiff', 'mp3', 'trueaudio', 'wave']):
                mu.getTags(mime, file, self.aiffTag)
            elif mime == 'mp4':
                self.orig_artist.setEnabled(False)
                self.language.setEnabled(False)
                mu.getTags(mime, file, self.mp4tag)
            elif mime == 'monkeysaudio':
                mu.getTags(mime, file, self.apeTag)
            elif mime == 'asf':
                mu.getTags(mime, file, self.asfTag)
            elif mime == 'musepack':
                mu.getTags(mime, file, self.mpcTag)
            else:
                mu.getTags(mime, file, self.general)

            self.support = True

    # Verificando se o arquivo é suportado pelo mutagen
    def isFileSupported(self):
        return self.support
