import os
import sys
import random
from pathlib import Path

from launchbox import existGame
import yt_dlp

listStatus = []
cls = lambda: os.system("cls")


def clear(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path):
            os.remove(path)


def searchYouTube(key):
    """Retorna o video_id do 1º resultado (busca + 'no commentary')."""
    query = f"ytsearch1:{key} no commentary"
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
    entries = info.get("entries") or []
    if not entries or not entries[0].get("id"):
        raise RuntimeError(f"Nenhum resultado no YouTube para: {key}")
    return entries[0]["id"]


def progress_hook(fileName):
    def _hook(d):
        if d.get("status") != "downloading":
            return
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        downloaded = d.get("downloaded_bytes") or 0
        current = (downloaded / total) if total else 0
        percent = f"{current * 100:.1f}"
        progress = int(50 * current)
        bar = "█" * progress + "-" * (50 - progress)
        for f in listStatus:
            if f["title"] == fileName:
                f["status"] = bar
                f["percent"] = percent
        cls()
        out = ""
        for f in listStatus:
            out += "{percent}|{status}|{title}\n".format(
                status=f["status"],
                percent=(f["percent"] + "%").ljust(6),
                title=f["title"],
            )
        sys.stdout.write(out)
        sys.stdout.flush()

    return _hook


def updateStatus(fileName, status):
    for f in listStatus:
        if f["title"] == fileName:
            f["status"] = status.ljust(50)


def _pick_range(duration, length, margin=60):
    """start/end em segundos; se o vídeo for curto, pega o que der."""
    if not duration or duration <= 0:
        return 0, float(length)
    length = min(float(length), float(duration))
    max_start = max(0.0, duration - length - margin)
    min_start = margin if max_start >= margin else 0.0
    start = (
        round(random.uniform(min_start, max_start), 2) if max_start > 0 else 0.0
    )
    end = min(start + length, duration)
    return start, end


def downloadClip(videoId, out_dir, fileName, length):
    out_mp4 = Path(out_dir) / f"{fileName}.mp4"
    if out_mp4.is_file():
        return True

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={videoId}"

    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        meta = ydl.extract_info(url, download=False)
    duration = meta.get("duration") or 0
    start, end = _pick_range(duration, length)

    updateStatus(fileName, f"Baixando {start:.0f}s–{end:.0f}s...")

    def ranges(info_dict, ydl):
        return [{"start_time": start, "end_time": end}]

    opts = {
        "outtmpl": str(Path(out_dir) / f"{fileName}.%(ext)s"),
        "format": (
            "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b"
        ),
        "merge_output_format": "mp4",
        "download_ranges": ranges,
        "force_keyframes_at_cuts": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_hook(fileName)],
        "noprogress": True,
        "postprocessor_args": {
            "ffmpeg": [
                "-vf",
                "scale=1280:720:force_original_aspect_ratio=decrease,"
                "pad=1280:720:(ow-iw)/2:(oh-ih)/2",
            ],
        },
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        updateStatus(fileName, str(e))
        return False

    if out_mp4.is_file():
        updateStatus(fileName, "Done")
        return True

    for p in Path(out_dir).glob(f"{fileName}.*"):
        if p.suffix.lower() in {".mp4", ".mkv", ".webm"}:
            if p != out_mp4:
                p.replace(out_mp4)
            updateStatus(fileName, "Done")
            return out_mp4.is_file()

    updateStatus(fileName, "Arquivo de saída não encontrado")
    return False


def gameDownload(game, directory, directoryOut, time):
    # directory: pasta temp limpa pelo __init__; o clipe vai em directoryOut.
    if existGame(game):
        return

    fileName = game.replace(":", "").replace("/", "")
    global listStatus
    listStatus.append({"status": "-" * 50, "percent": "0", "title": fileName})

    try:
        videoId = searchYouTube(game)
    except Exception as e:
        updateStatus(fileName, str(e))
        return

    downloadClip(videoId, directoryOut, fileName, time)
