# launcher-box-youtube-downloader

Script para o LaunchBox: lê o XML da plataforma, verifica se já existe vídeo/trailer local e baixa do YouTube o que faltar.

## Requisitos

- Python 3
- [ffmpeg](https://ffmpeg.org/) no PATH
- Dependências:

```bash
pip install -r requirements.txt
```

## Uso

Ajuste os paths em `launchbox.py` e `__init__.py` (`Z:\\LaunchBox\\...`) e rode:

```bash
python __init__.py
```

Por padrão baixa clipes de ~60s (trecho aleatório) em 1280×720 mp4 via **yt-dlp** (sem moviepy/pytube).
