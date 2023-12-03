import re

from PyQt5.QtCore import QObject, QFileInfo

from mutagen._file import File
from mutagen.aac import AAC
from mutagen.ac3 import AC3
from mutagen.aiff import AIFF
from mutagen.asf import ASF
from mutagen.flac import FLAC
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.musepack import Musepack
from mutagen.oggflac import OggFLAC
from mutagen.oggopus import OggOpus
from mutagen.oggspeex import OggSpeex
from mutagen.oggvorbis import OggVorbis
from mutagen.optimfrog import OptimFROG
from mutagen.trueaudio import TrueAudio
from mutagen.wave import WAVE
from mutagen.wavpack import WavPack
from mutagen.id3 import TPE1, TIT2, TALB, TCOP, TDRC, TRCK, TCON, TPE2, TPOS, TCOM, TOPE, TLAN, TENC, COMM, WXXX, \
    TXXX, WOAR, UrlFrame

########################################################################################################################

# Mutagen is a Python module to handle audio metadata.
# It supports ASF, FLAC, MP4, Monkey’s Audio, MP3, Musepack, Ogg Opus, Ogg FLAC, Ogg Speex, Ogg Theora, Ogg Vorbis,
# True Audio, WavPack, OptimFROG, and AIFF audio files.

########################################################################################################################


# Classe para manipulação de arquivos multimídia suportado pelo mutagen
class MU(QObject):
    def __init__(self):
        super().__init__()
        self.endtrack = 0

        self.allTags = [
            'artist',          # 0
            'title',           # 1
            'album',           # 2
            'discnumber',      # 3
            'albumartist',     # 4
            'genre',           # 5
            'date',            # 6
            'tracknumber',     # 7
            'tracktotal',      # 8
            'composer',        # 9
            'originalartist',  # 10
            'copyright',       # 11
            'language',        # 12
            'encoded-by',      # 13
            'website',         # 14
            'comment'          # 15
        ]

        tagmp3 = {
            'artist': ['TPE1', TPE1],
            'title': ['TIT2', TIT2],
            'album': ['TALB', TALB],
            'discnumber': ['TPOS', TPOS],
            'albumartist': ['TPE2', TPE2],
            'genre': ['TCON', TCON],
            'date': ['TDRC', TDRC],
            'tracknumber': ['TRCK', TRCK],
            'tracktotal': ['TXXX:TRACKTOTAL', TXXX],  # desc='TRACKTOTAL'
            'composer': ['TCOM', TCOM],
            'originalartist': ['TOPE', TOPE],
            'copyright': ['TCOP', TCOP],
            'language': ['TLAN', TLAN],
            'encoded-by': ['TENC', TENC],
            'website': ['WXXX:', WXXX],  # desc='', url=''
            'comment': ['COMM::eng', COMM]  # lang='eng', desc=''
        }

        tagmpc = {
            'artist': 'ARTIST',
            'title': 'TITLE',
            'album': 'ALBUM',
            'discnumber': 'DISCNUMBER',
            'albumartist': 'ALBUMARTIST',
            'genre': 'GENRE',
            'date': 'YEAR',
            'tracknumber': 'TRACK',
            'tracktotal': 'TRACKTOTAL',
            'composer': 'COMPOSER',
            'originalartist': 'ORIGINALARTIST',
            'copyright': 'COPYRIGHT',
            'language': 'LANGUAGE',
            'encoded-by': 'ENCODED-BY',
            'website': 'WEBSITE',
            'comment': 'COMMENT'
        }

        tagape = {
            'artist': 'Artist',
            'title': 'Title',
            'album': 'Album',
            'discnumber': 'Part',
            'albumartist': 'Album Artist',
            'genre': 'Genre',
            'date': 'Year',
            'tracknumber': 'Track',  # tracktotal
            'composer': 'Composer',
            'originalartist': 'Original Artist',
            'copyright': 'Copyright',
            'language': 'Language',
            'encoded-by': 'Encoded By',
            'website': 'Related',
            'comment': 'Comment'
        }

        tagmp4 = {
            'artist': '©ART',
            'title': '©nam',
            'album': '©alb',
            'discnumber': 'disk',
            'albumartist': 'aART',
            'genre': '©gen',
            'date': '©day',
            'tracknumber': 'trkn',
            'composer': '©wrt',
            'copyright': 'cprt',
            'encoded-by': '©enc',
            'website': 'purl',
            'comment': '©cmt'
        }

        tagasf = {
            'artist': 'Author',
            'title': 'Title',
            'album': 'WM/AlbumTitle',
            'discnumber': 'WM/PartOfSet',
            'albumartist': 'WM/AlbumArtist',
            'genre': 'WM/Genre',
            'date': 'WM/Year',
            'tracknumber': 'WM/TrackNumber',  # tracktotal
            'composer': 'WM/Composer',
            'originalartist': 'WM/OriginalArtist',
            'copyright': 'Copyright',
            'language': 'WM/Language',
            'encoded-by': 'WM/EncodedBy',
            'website': 'WM/AuthorURL',
            'comment': 'Description'
        }

        self.supported = (
            ['aac', AAC, {}],                        # 0  aac
            ['ac3', AC3, {}],                        # 1  ac3
            ['aiff', AIFF, tagmp3],                  # 2  aiff
            ['asf', ASF, tagasf],                    # 3  asf, wma
            ['flac', FLAC, self.allTags],            # 4  flac
            ['monkeysaudio', MonkeysAudio, tagape],  # 5  ape
            ['mp3', MP3, tagmp3],                    # 6  mp3
            ['mp4', MP4, tagmp4],                    # 7  m4a, mp4
            ['musepack', Musepack, tagmpc],          # 8  mpc
            ['oggflac', OggFLAC, self.allTags],      # 9  ogg
            ['oggopus', OggOpus, self.allTags],      # 10 ogg, opus
            ['oggspeex', OggSpeex, self.allTags],    # 11 ogg
            ['oggvorbis', OggVorbis, self.allTags],  # 12 ogg
            ['optimfrog', OptimFROG, {}],            # 13 ofr
            ['trueaudio', TrueAudio, tagmp3],        # 14 tta
            ['wave', WAVE, tagmp3],                  # 15 wav
            ['wavpack', WavPack, tagape]             # 16 wv
        )

########################################################################################################################

    # Função para verificar se a mídia é suportada pelo mutagen e se foi implementado no projeto
    def is_supported(self, file):
        try:
            s = self.supported[self.idx(self.supported, str(File(file).info)[1:].split(' ')[0].split('.')[1])][0]
            print(f'(\033[92mmutagen_utils\033[m) select: {s}')
            return s
        except Exception as msg:
            print(f'(\033[92mmutagen_utils\033[m) {msg}')
            return None

    # Usada para retornar posição de uma array dentro de outra array
    @staticmethod
    def idx(array, string):
        i = 0
        for sub_array in array:
            if string in sub_array:
                return i
            i += 1
        return -1

    # Função que retorna true quando uma das opções coincidir
    @staticmethod
    def regex(mime, patern):
        if re.search(patern, mime.lower(), re.IGNORECASE):
            return True
        return False

    # Função para retornar a ordem das id tags
    def order_tags(self):
        return self.allTags

    # Função usada para a leitura de tags dos mais diversos formatos e padrões
    def get_tags(self, mime, file, edit) -> None:
        media = {}

        try:
            for sub in self.supported:
                if mime == sub[0]:
                    media = sub[1](file)
                    break
        except Exception as msg:  # tentando pelo sufixo em caso de engano
            print(f'(\033[92mmutagen_utils\033[m) {msg}')
            s = self.supported[self.idx(self.supported, QFileInfo(file).suffix())][0]
            print(f'(\033[92mmutagen_utils\033[m) select: {s}')
            for sub in self.supported:
                if s == sub[0]:
                    try:
                        media = sub[1](file)
                    except Exception as msg:
                        _ = msg
                        pass
                    break
            pass

        # debug não tirar
        print(f'(\033[92mmutagen_utils\033[m) {media}')

        for tag in edit:
            if tag[0].text() != '':
                continue

            try:

                if self.regex(mime, r'asf|aiff|mp3|trueaudio|wave'):
                    r = re.compile(tag[1] + ':+.*|' + tag[1] + '$', re.IGNORECASE)
                    tags = media[list(filter(r.match, media.keys()))[0]]
                else:
                    tags = media[tag[1]]

                if tags is not None:
                    if self.regex(tag[1], r'tracknumber|trck|trkn|^track$') and self.endtrack == 0:
                        self.endtrack = 1
                        print(f'(\033[92mmutagen_utils\033[m) endtrack value: {self.endtrack}')
                        if tag[1] == 'trkn':
                            tag[0].setText(str(tags[0][0]))
                        else:
                            tag[0].setText(str(tags[0]).split('/')[0])
                    elif self.regex(tag[1], r'tracknumber|trck|trkn|^track$') and self.endtrack == 1:
                        self.endtrack = 0
                        print(f'(\033[92mmutagen_utils\033[m) endtrack value: {self.endtrack}')
                        if tag[1] == 'trkn':
                            tag[0].setText(str(tags[0][1]) if tags[0][1] != 0 else '')
                        else:
                            tag[0].setText(str(tags[0]).split('/')[1])
                    elif tag[1] == 'disk' and mime == 'mp4':
                        tag[0].setText(str(tags[0][0]) if tags[0][0] != 0 else '')
                    else:
                        if self.regex(mime, r'aiff|mp3|trueaudio|wave'):
                            tag[0].setText(str(tags))
                        else:
                            tag[0].setText(str(tags[0]))
            except Exception as msg:
                _ = msg
                pass

    # Função para alterar as tags automaticamente após requisições
    def apply_tags(self, mime='', file=None, keys=None) -> None:
        media = {}
        model = {}

        try:
            for sub in self.supported:
                if mime == sub[0]:
                    media = sub[1](file)
                    model = sub[2]
                    break
        except Exception as msg:  # tentando pelo sufixo em caso de engano
            print(f'(\033[92mmutagen_utils\033[m) {msg}')
            s = self.supported[self.idx(self.supported, QFileInfo(file).suffix())][0]
            print(f'(\033[92mmutagen_utils\033[m) select: {s}')
            for sub in self.supported:
                if s == sub[0]:
                    try:
                        media = sub[1](file)
                    except Exception as msg:
                        _ = msg
                        pass
                    break
            pass

        # debug não tirar
        print(f'(\033[92mmutagen_utils\033[m) {media}')
        print(f'(\033[92mmutagen_utils\033[m) {keys}')

        for tags in self.allTags:
            try:
                tag = model.get(tags) if type(model) == dict else None
                if tag is not None and keys.get(tags) is not None:
                    if self.regex(mime, r'aiff|mp3|trueaudio|wave'):
                        if tags == 'tracktotal':
                            media[tag[0]] = tag[1](encoding=3, desc='TRACKTOTAL', text=keys.get(tags))
                        elif tags == 'website':
                            if mime == 'mp3':
                                media[tag[0]] = tag[1](encoding=3, desc='', url=keys.get(tags))
                            else:

                                r = [i for i in media if re.match(r'^WOAR:.*|^WOAR.*', i)]
                                for i in r:
                                    media.pop(i, None)
                                media[f'WOAR:{keys.get(tags)}'] = WOAR(UrlFrame(keys.get(tags)))

                        elif tags == 'comment':
                            media[tag[0]] = tag[1](encoding=3, lang='eng', desc='', text=keys.get(tags))
                        else:
                            media[tag[0]] = tag[1](encoding=3, text=keys.get(tags))
                    elif self.regex(mime, r'mp4|asf|monkeysaudio|musepack|wavpack'):
                        if tags == 'discnumber' and mime == 'mp4':
                            print('foi')
                            media[tag] = [(int(keys.get(tags)), 0)]
                        elif tags == 'tracknumber' and self.regex(mime, r'mp4|asf|monkeysaudio|wavpack'):
                            if mime == 'mp4':
                                t = 0 if keys.get('tracktotal') == '' else int(keys.get('tracktotal'))
                                media[tag] = [(int(keys.get(tags)), t)]
                            elif self.regex(mime, r'asf|monkeysaudio|wavpack'):
                                media[tag] = f'{keys.get(tags)}/{keys.get("tracktotal")}'
                        else:
                            media[tag] = keys.get(tags)
                else:
                    if self.regex(mime, r'flac|ogg'):  # padrão vorbis
                        media[tags] = keys.get(tags)

            except Exception as msg:
                print(f'(\033[92mmutagen_utils\033[m) {msg}')
                pass

        media.save()
