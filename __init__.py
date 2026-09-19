from functions import clear, gameDownload
from launchbox import getGames
import os
from joblib import Parallel, delayed

cls = lambda: os.system("cls")
directory = "videos"
directoryOut = "Z:\\LaunchBox\\Videos\\Windows"
jobs = 10
time = 60  # segundos do clipe
clear(directory)

games = getGames("Windows")
cls()

Parallel(n_jobs=jobs, require="sharedmem")(
    delayed(gameDownload)(game, directory, directoryOut, time) for game in games
)
