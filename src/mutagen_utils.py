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
from mutagen.id3 import TPE1, TIT2, TALB, TCOP, TDRC, TRCK, TCON, TPE2, TPOS, TCOM, TOPE, TLAN, TENC, COMM, WXXX, TXXX

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
            'encodedby',       # 13
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
            'encodedby': ['TENC', TENC],
            'website': ['WXXX:', WXXX],  # desc='', url=''
            'comment': ['COMM::eng', COMM]  # lang='eng', desc=''
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
            'encodedby': '©enc',
            'website': 'purl',
            'comment': '©cmt'
        }

        self.supported = (
            ['aac', AAC, {}],                    # 0  aac
            ['ac3', AC3, {}],                    # 1  ac3
            ['aiff', AIFF, {}],                  # 2  aiff
            ['asf', ASF, {}],                    # 3  asf, wma
            ['flac', FLAC, {}],                  # 4  frac
            ['monkeysaudio', MonkeysAudio, {}],  # 5  ape
            ['mp3', MP3, tagmp3],                # 6  mp3
            ['mp4', MP4, tagmp4],                # 7  m4a, mp4
            ['musepack', Musepack, {}],          # 8  mpc
            ['oggflac', OggFLAC, {}],            # 9  ogg
            ['oggopus', OggOpus, {}],            # 10 ogg, opus
            ['oggspeex', OggSpeex, {}],          # 11 ogg
            ['oggvorbis', OggVorbis, {}],        # 12 ogg
            ['optimfrog', OptimFROG, {}],        # 13 ofr
            ['trueaudio', TrueAudio, {}],        # 14 tta
            ['wave', WAVE, {}],                  # 15 wav
            ['wavpack', WavPack, {}]             # 16 wv
        )

########################################################################################################################

    # Função para verificar se a mídia é suportada pelo mutagen e se foi implementado no projeto
    def isSupported(self, file):
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

    # Função para retornar a ordem das id tags
    def orderTags(self):
        return self.allTags

    # Função usada para a leitura de tags dos mais diversos formatos e padrões
    def getTags(self, mime, file, edit) -> None:
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
            if tag[0].text() != str(): continue

            try:

                if self.equal(mime, ['asf', 'aiff', 'mp3', 'trueaudio', 'wave']):
                    r = re.compile(tag[1] + ':+.*|(wm/)*' + tag[1] + '$', re.IGNORECASE)
                    tags = media[list(filter(r.match, media.keys()))[0]]
                else:
                    tags = media[tag[1]]

                if tags is not None:
                    tk = ['tracknumber', 'TRCK', 'trkn', 'track']

                    if self.equal(tag[1], tk) and self.endtrack == 0:
                        self.endtrack = 1
                        if tag[1] == 'trkn':
                            tag[0].setText(str(tags[0][0]))
                        else:
                            tag[0].setText(str(tags[0]).split('/')[0])
                    elif self.equal(tag[1], tk) and self.endtrack == 1:
                        self.endtrack = 0
                        if tag[1] == 'trkn':
                            tag[0].setText(str(tags[0][1]))
                        else:
                            tag[0].setText(str(tags[0]).split('/')[1])
                    elif tag[1] == 'disk' and mime == 'mp4':
                        tag[0].setText(str(tags[0][0]))
                    else:
                        if self.equal(mime, ['aiff', 'mp3', 'trueaudio', 'wave']):
                            tag[0].setText(str(tags))
                        else:
                            tag[0].setText(str(tags[0]))
            except Exception as msg:
                _ = msg
                pass

    # Função que retorna true quando uma das opções coincidir
    @staticmethod
    def equal(mime, array):
        for i in array:
            if mime.lower() == i.lower():
                return True
        return False

    # Função para alterar as tags automaticamente após requisições
    def applyTags(self, mime=str(), file=None, keys=None) -> None:
        media = {}
        model = {}

        try:
            for sub in self.supported:
                if mime == sub[0]:
                    media = sub[1](file)
                    model = sub[2]
                    break
        except Exception as msg:  # tentando pelo sufixo em caso de engano
            print(msg)
            s = self.supported[self.idx(self.supported, QFileInfo(file).suffix())][0]
            print('select: ' + s)
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
                tag = model.get(tags)
                if tag is not None and keys.get(tags) is not None:
                    if mime == 'mp3':
                        if tags == 'tracktotal':
                            media[tag[0]] = tag[1](encoding=3, desc='TRACKTOTAL', text=keys.get(tags))
                        elif tags == 'website':
                            media[tag[0]] = tag[1](encoding=3, desc='', url=keys.get(tags))
                        elif tags == 'comment':
                            media[tag[0]] = tag[1](encoding=3, lang='eng', desc='', text=keys.get(tags))
                        else:
                            media[tag[0]] = tag[1](encoding=3, text=keys.get(tags))
                    elif mime == 'mp4':
                        media[tag] = keys.get(tags)
            except Exception as msg:
                print(msg)
                pass

        media.save()
