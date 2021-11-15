import moviepy.editor
import os, sys, random, re
import urllib.request
from pytube import YouTube
from launchbox import existGame
import time
from pathlib import Path

listStatus = []
cls = lambda: os.system('cls')
def clear(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))

def seachYouTube(key):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+key.replace(' ','+')+'+no+commentary')
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return video_ids[0]

def progress_function(fileName, chunk, file_handle, bytes_remaining):
    global listStatus
    current = ((chunk.filesize - bytes_remaining)/chunk.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)

    for f in listStatus:
        if(f['title']==fileName):
            f['status'] = status
            f['percent'] = str(percent)
    
    cls()
    status = ''
    for f in listStatus:
        status +='{percent}|{status}|{title}\n'.format(status=f['status'], percent=(f['percent']+"%").ljust(6),title=f['title'])
    
    sys.stdout.write(status)
    sys.stdout.flush()
    time.sleep(3)
    
def downloadYouTube(videoId, path, fileName):
    my_file = Path(path+fileName+".mp4")
    if my_file.is_file():
        return True
    
    videourl = 'https://www.youtube.com/watch?v='+videoId
    yt = YouTube(videourl, on_progress_callback=lambda chunk, file_handle, bytes_remaining: progress_function(fileName, chunk, file_handle, bytes_remaining))
    listYt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    yt = listYt.first()
    try:
        yt.download(path, filename=fileName+".mp4")
    except Exception as e:
        updateStatus(fileName, str(e))
        return False
    
    return True

def CutVideos(fileName, directory, directoryOut, length):
    xdim = 1280
    ydim = 720
    ext = ".mp4"
    
    updateStatus(fileName, 'Cutting Video...')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # import to moviepy
    clip = moviepy.editor.VideoFileClip(directory + "\\" + fileName + ext).resize( (xdim, ydim) ) 

    cut = 60
    # select a random time point
    start = round(random.uniform(cut,clip.duration-length-cut), 2) 

    # cut a subclip
    out_clip = clip.subclip(start,start+length)

    outfile = directoryOut+"\\"+fileName+ext
    out_clip.write_videofile(outfile)
    
    updateStatus(fileName, 'Done')

def updateStatus(fileName, status):
    for f in listStatus:
        if(f['title']==fileName):
            f['status'] = status.ljust(50)

def gameDownload(game, directory, directoryOut, time):
    if existGame(game):
        return
    
    videoId = seachYouTube(game)
    fileName = game.replace(":","").replace("/","")
    global listStatus
    listStatus.append({'status':'-' * 50, 'percent':"0", 'title':fileName})
    
    if(downloadYouTube(videoId, directory, fileName)):
        CutVideos(fileName, directory, directoryOut, time)