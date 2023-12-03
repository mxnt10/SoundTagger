# SoundTagger

Programa que tem por objetivo não apenas usar impressão digital acústica para buscar por nomes de musicas, mas também
usar essas requisições para alterar o metadata (id tag) dos arquivos e se preferir, renomear os arquivos multimídia
conforme os resultados obtidos.

### Suporte de Mídias Testados 

✅️ Suportado 🟥 Não suportado 🟨 Não testado/implementado

| Formatos       | mutagen(view) | mutagen(edit) | acoustID | audD.io |
|----------------|:-------------:|:-------------:|:--------:|:-------:|
| `aac`          |      🟨       |      🟨       |    🟨    |   🟨    |
| `ac3`          |      🟨       |      🟨       |    🟨    |   🟨    |
| `aiff`         |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `ape`          |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `asf wma`      |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `flac`         |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `mp3`          |      ✅️       |      ✅️       |    ✅️    |   ✅️    |
| `mp4 m4a`      |      ✅️       |      ✅️       | ✅️ `m4a` |   🟨    |
| `mpc`          |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `ofr ofs`      |      🟨       |      🟨       |    🟥    |   🟨    |
| `ogg ogv opus` |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `tta`          |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `wav`          |      ✅️       |      ✅️       |    🟨    |   🟨    |
| `wv`           |      ✅️       |      ✅️       |    🟨    |   🟨    |
 
### Recursos do Programa até o Momento

✅️️ Implementado 🟥 Não implementado 🟦 Preparando 🟨 Instável ou limitado

| Recursos                                                | Implementação |
|---------------------------------------------------------|:-------------:|
| Editor de metadatas (ID Tags)                           |      🟦       |
| Editor de metadatas avançado (ID Tags)                  |      🟥       |
| Pesquisa de fingerprint via arquivos de áudio           |      ✅️       |
| Pesquisa de fingerprint via escuta ( microfone )        |      🟥       |
| Pesquisa de fingerprint de links de áudio               |      🟥       |
| Pesquisa de fingerprint de músicas presente em vídeos   |      🟥       |
| Selecionar parte dos arquivos de áudio para requisições |      ✅️       |
| Lista de requisições realizadas                         |      🟥       |
| Exportar Lista de requisições realizadas                |      🟥       |
| Seleção de arquivos específicos para as requisições     |      ✅️️      |
| Suporte a API audD.io                                   |      ✅️️      |
| Suporte a API acoustID                                  |      ✅️️      |
| Suporte a API ACRCloud                                  |      🟥       |
| Pesquisa via ShazamKit                                  |      🟥       |
| Renomear arquivos após requisições se preferir          |      ✅️️      |
| Inserir tags após requisições se preferir               |      🟦       |
| Reprodutor de mídia integrado                           |      🟥       |
| Multiprocessamento (Requisições em massa)               |      ✅️       |
| Opção de customização geral do programa                 |      🟥       |
| Ajuste das opções de multiprocessamento                 |      🟥       |
| Ajustes indivíduais para cada arquivo se necessário     |      🟥       |
| Suporte a Notificações                                  |      🟨️      |
| Converter formatos menos comuns para os mais comuns     |      🟥       |

### Dependências Usadas no Programa

✅️️ Inclusas no programa 🟧 Precisa instalar no sistema 🟦 Presentes no sistema

|             Dependências do Programa | Versão Usada | Inclusão |
|-------------------------------------:|:------------:|:--------:|
|                              mutagen |    1.46.0    |   ✅️️    |
|                                plyer |    2.1.0     |   ✅️️    |
|                           pyacoustid |    1.2.2     |   ✅️️    |
|                                pydub |    0.25.1    |   ✅️️    |
|                                PyQt5 |    5.15.2    |    🟧    |
|                              superqt |    0.4.1     |   ✅️️    |
|                          qt5 (PyQt5) |    5.15.3    |    🟧    |
|             chromaprint (pyacoustid) |    1.5.1     |    🟧    |
|                       ffmpeg (pydub) |    4.4.1     |    🟧    |
|      requests (presente nas distros) |    2.26.0    |    🟦    |
| python (nem precisaria citar mas...) |    3.9.10    |    🟦    |
