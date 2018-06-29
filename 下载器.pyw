import requests, os, time, random
from 目录编辑器 import removeItem
from datetime import datetime
from time import strftime
from pytz import timezone

def main():
    filePath = "index.txt"
    file = open(filePath, "r")
    videoList = processFile(file)
    download(videoList)

def processFile(file):
    vNL, iNL, eL = [], [], []

    for line in file.readlines():
        vN, iN, e = line.split("  ")

        if "\n" in e:
            e = e[:-1]

        vNL.append(vN)
        iNL.append(iN)
        eL.append(e)

    videoList = []
    
    for i in range(len(vNL)):
        videoList.append([iNL[i], eL[i], vNL[i]])

    return videoList

def download(videoList):
    for l in videoList:
        episode, indexNumber = l[1], l[0]
        attempt = True
        
        url = "http://diaodiaode.me/rss/feed/" + str(indexNumber)

        r = requests.get(url)

        if episode == "S00E00":
            index = r.text.find("中英字幕")
        else:
            episode1 = str(episode) + ".中英字幕"
            index = r.text.find(episode1)
        if index == -1:
            episode = str(episode) + ".END.中英字幕"
            index = r.text.find(episode)
            if index == -1:
                attempt = False

        if attempt:
            text = r.text[index:]
            index1 = text.find("<magnet>")
            index2 = text.find("</magnet>")
            magnetLink = text[index1 + 8:index2]
            os.startfile(magnetLink)
            changeFile(l[1], l[0], l[2], videoList)
            createLog(l[1], l[2])
            
def createLog(episode, videoName):
    filePath = "log.txt"
    file = open(filePath, "r")
    lines = file.readlines()
    file.close()

    oldLine = []
    
    for line in lines:
        if "\n" in line:
            line = line[:-1]

        oldLine.append(line)

    time = datetime.now(timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
    newLine = time + " GMT+8 " + videoName + " " + episode

    oldLine.append(newLine)
    lines = oldLine

    file = open(filePath, "w")
    for line in lines:
        print(line, file = file)
    file.close()

def changeFile(episode, indexNumber, videoName, videoList):
    r = requests.get("http://diaodiaode.me/rss/feed/" + str(indexNumber))
    
    if episode == "S00E00" or r.text.find("本剧完结") != -1:
        removeItem(indexNumber)
        createLog("Removed", videoName)
    else:
        oldEpisode = episode
        episode = episode[1:]
        season, episode = episode.split("E")
        
        if r.text.find("连载中") != -1:
            episode = int(episode) + 1
        elif r.text.find("季完结") != -1:
            season = int(season) + 1
            episode = 1

        if len(str(season)) == 1:
            sN = "0" + str(season)
        else:
            sN = str(season)

        if len(str(episode)) == 1:
            eN = "0" + str(episode)
        else:
            eN = str(episode)

        episode = "S" + sN + "E" + eN
      
        index = videoList.index([indexNumber, oldEpisode, videoName])
        videoList[index] = [indexNumber, episode, videoName]

        file = open("index.txt", "w")

        for i in range(len(videoList)):
            print(videoList[i][2] + "  " + videoList[i][0] + "  " + videoList[i][1],
                  file = file)

        file.close()
    

if __name__ == "__main__":
    while True:
        main()
        time.sleep(random.randrange(1, 15) * 60)
