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


# Classe para manipulação de arquivos multimídia suportado pelo mutagen
class MU(QObject):
    def __init__(self):
        super().__init__()
        self.endtrack = 0

        self.supported = [
            ['aac', AAC],               # 0  aac
            ['ac3', AC3],                # 1  ac3
            ['aiff', AIFF],               # 2  aiff
            ['asf', ASF],                  # 3  asf, wma
            ['flac', FLAC],                 # 4  frac
            ['monkeysaudio', MonkeysAudio],  # 5  ape
            ['mp3', MP3],                    # 6  mp3
            ['mp4', MP4],                    # 7  m4a, mp4
            ['musepack', Musepack],          # 8  mpc
            ['oggflac', OggFLAC],            # 9  ogg
            ['oggopus', OggOpus],            # 10 ogg, opus
            ['oggspeex', OggSpeex],          # 11 ogg
            ['oggvorbis', OggVorbis],        # 12 ogg
            ['optimfrog', OptimFROG],        # 13 ofr
            ['trueaudio', TrueAudio],        # 14 tta
            ['wave', WAVE],                  # 15 wav
            ['wavpack', WavPack]             # 16 wv
        ]

    # Função para verificar se a mídia é suportada pelo mutagen e se foi implementado no projeto
    def isSupported(self, file):
        try:
            s = self.supported[self.idx(self.supported, str(File(file).info)[1:].split(' ')[0].split('.')[1])][0]
            print('select: ' + s)
            return s
        except Exception as msg:
            print(msg)
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

    # Função usada para a leitura de tags dos mais diversos formatos e padrões
    def getTags(self, mime, file, edit) -> None:
        media = {}

        try:
            for sub in self.supported:
                if mime == sub[0]:
                    media = sub[1](file)
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
        print(media)

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
