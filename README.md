# SoundTagger

Programa que tem por objetivo não apenas usar impressão digital acústica para buscar por nomes de musicas, mas também
usar essas requisições para alterar o metadata (id tag) dos arquivos e se preferir, renomear os arquivos multimídia
conforme os resultados obtidos.
 
### Recursos do Programa️️

| Recursos Implementados                                  | ✔️ Ok ❌ No ➕ Next ➖ Unstable |
|---------------------------------------------------------|:----------------------------:|
| Pesquisa de som via arquivos de áudio                   |              ✔️              |
| Pesquisa de som via escuta ( microfone )                |              ❌               |
| Pesquisa de som de links de áudio                       |              ❌               |
| Lista de requisições realizadas                         |              ❌               |
| Seleção de arquivos específicos para as requisições     |              ✔️              |
| Suporte a API audD.io                                   |              ✔️              |
| Suporte a API acoustID                                  |              ✔️              |
| Suporte a API ACRCloud                                  |              ❌               |
| Pesquisa via ShazamKit                                  |              ❌               |
| Renomear arquivos após requisições se preferir          |              ✔️              |
| Inserir tags após requisições se preferir               |              ✔️              |
| Reprodutor de mídia integrado                           |              ❌               |
| Multiprocessamento (Requisições em massa)               |              ✔️              |
| Selecionar parte dos arquivos de áudio para requisições |              ✔️              |
| Buscar áudio das músicas presente nos vídeos            |              ❌               |
| Opção de customizar a fonte do programa                 |              ❌               |
| Opção de customizar o plano de fundo do programa        |              ❌               |
| Ajuste das opções de multiprocessamento                 |              ❌               |
| Ajustes indivíduais para cada arquivo se necessário     |              ❌               |
| Suporte a Notificações                                  |              ✔️              |

|             Dependências do Programa | Versão Usada | ✔️ Incluso ➕ Faltante ➖ Sistema |
|-------------------------------------:|:------------:|:-------------------------------:|
|                              mutagen |    1.46.0    |               ✔️                |
|                                plyer |    2.1.0     |               ✔️                |
|                           pyacoustid |    1.2.2     |                ➕                |
|                                pydub |    0.25.1    |               ✔️                |
|                                PyQt5 |    5.15.2    |                ➕                |
|                              superqt |    0.4.1     |                ➕                |
|                          qt5 (PyQt5) |    5.15.3    |                ➕                |
|             chromaprint (pyacoustid) |    1.5.1     |                ➕                |
|                       ffmpeg (pydub) |    4.4.1     |                ➕                |
|      requests (presente nas distros) |    2.26.0    |                ➖                |
| python (nem precisaria citar mas...) |    3.9.10    |                ➖                |
