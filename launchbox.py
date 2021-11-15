import xml.etree.ElementTree as ET
from pathlib import Path

xmlFile = 'Z:\\LaunchBox\\Data\\Platforms'
directoryVideos='Z:\\LaunchBox\\Videos\\Windows\\'

def getGames(plataform):
    # parse an xml file by name
    tree = ET.parse(xmlFile+"\\"+plataform+".xml")
    root = tree.getroot()

    games=[]

    # all items data
    for elem in root:
        title = elem.find('Title')
        hide = elem.find('Hide')
        if(title is not None):
            if(hide.text != "true"):
                games.append(title.text)
    return games

def existGame(game):
    if existVideo(game, "webm"):
        return True
    if existVideo(game, "mp4"):
        return True
    if existVideo("Trailer\\"+game, "webm"):
        return True
    if existVideo("Trailer\\"+game, "mp4"):
        return True

def existVideo(game, ext):
    my_file = Path(directoryVideos+game+"."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game+"-01."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace(":","")+"."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace(":","")+"-01."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace(":","_")+"."+ext)
    if my_file.is_file():
        return True

    my_file = Path(directoryVideos+game.replace(":","_")+"-01."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace(" ","_")+"-01."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace(" ","_")+"."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace("'","_")+"."+ext)
    if my_file.is_file():
        return True
    my_file = Path(directoryVideos+game.replace("'","_")+"-01."+ext)
    if my_file.is_file():
        return True
    
    my_file = Path(directoryVideos+game.replace("'","_").replace(":","_")+"."+ext)
    if my_file.is_file():
        return True
    my_file = Path(directoryVideos+game.replace("'","_").replace(":","_")+"-01."+ext)
    if my_file.is_file():
        return True
    return False