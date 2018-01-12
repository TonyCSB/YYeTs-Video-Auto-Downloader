import requests
import os

filePath = "index.txt"

def main():
    print("欢迎使用人人影视自动下载器 - 目录编辑器    - By Tony")
    while True:
        choice = printIntro()
        select(choice)

def printIntro():
    print("\n请使用数字键选择以下选项：")
    print("1. 查询列表")
    print("2. 增加项目")
    print("3. 删除项目")
    print("4. 更新进度")
    print("5. 退出程序\n")

    while True:
        try:
            choice = input()
            if 1 <= int(choice) <= 5:
                choice = int(choice)
                return choice
            
        except:
            pass

def select(choice):
    print()
    
    if choice == 1:
        printList()
    elif choice == 2:
        addItem()
    elif choice == 3:
        removeItem(1)
    elif choice == 4:
        printFile()
    else:
        exit

def printList():
    videoName, indexNumber, episode = processFile()
    for i in range(len(videoName)):
        print("{0:3}  {1:50}".format(str(i + 1) + ".", videoName[i]))

def addItem():
    print("请输入想要添加的影视剧的代码：\n")

    vNL, iNL, eL = processFile()
    
    while True:
        index = input()

        if index == "":
            return False
        
        try:
            index = int(index)
            if len(str(index)) == 5 and str(index) not in iNL:
                break
            
        except ValueError:
            pass

        if str(index) in iNL:
            print("该影视剧已存在与数据库中\n")

    url = "http://diaodiaode.me/rss/feed/" + str(index)

    r = requests.get(url)
    index1 = r.text.find("<title>")

    if index1 == -1:
        print("该影视剧不存在")
        return True
    
    text = r.text[index1:]
    index1 = text.find("《")
    index2 = text.find(")")
    videoName = text[index1:index2 + 1]

    if "&apos;" in videoName:
        videoName = videoName.replace("&apos;", "'")
    
    indexNumber = index

    print("\n是否提取最新剧集？(Y/N)\n")

    while True:
        answer = input()
        if answer.lower()[0] == "y":
            break
        elif answer.lower()[0] == "n":
            break

    if answer.lower()[0] == "y":
        episode = returnEpisode(url)
    else:
        print("请输入最后观看剧集：（以S0xE0x的形式输入）\n")
        episode = input()

    vNL.append(videoName)
    iNL.append(str(indexNumber))
    eL.append(episode)

    sortList = []
    
    for i in range(len(vNL)):
        sortList.append([iNL[i], vNL[i], eL[i]])

    sortList.sort()

    file = open(filePath, mode = "w")

    for i in range(len(vNL)):
        print(sortList[i][1] + "  " + sortList[i][0] + "  " + sortList[i][2],
              file = file)

    file.close()

def removeItem(n):
    if n == 1:
        printList()
        print("\n请输入想要删除的影视剧的代码\n")

        while True:
            index = input()

            if index == "":
                return False
            
            try:
                index = int(index)
                if index >= 1:
                    break

            except ValueError:
                pass

        index = index - 1
    
    vNL, iNL, eL = processFile()
    
    sortList = []

    if n != 1:
        index = iNL.index(n)
    
    for i in range(len(vNL)):
        sortList.append([iNL[i], vNL[i], eL[i]])

    del sortList[index]

    file = open(filePath, mode = "w")

    for i in range(len(vNL) - 1):
        print(sortList[i][1] + "  " + sortList[i][0] + "  " + sortList[i][2],
              file = file)

    file.close()

def printFile():
    vNL, iNL, eL = processFile()

    episodeList = []

    for i in range(len(eL)):
        episode = returnEpisode("http://diaodiaode.me/rss/feed/" + str(iNL[i]))
        episodeList.append(episode)

    file = open(filePath, mode = "w")

    for i in range(len(vNL)):
        print(vNL[i] + "  " + iNL[i] + "  " + episodeList[i], file = file)
    
def processFile():
    file = open(filePath, mode = "r")
    vNL, iNL, eL = [], [], []
    
    for line in file.readlines():
        vN, iN, e = line.split("  ")

        if "\n" in e:
            e = e[:-1]
        
        vNL.append(vN)
        iNL.append(iN)
        eL.append(e)

    file.close()
        
    return vNL, iNL, eL

def returnEpisode(url):
    r = requests.get(url)

    seasonNumber, eN = 0, 0

    if "Doctor Who" in r.text:
        seasonNumber = 9
    
    episode = "S01E01"

    if r.text.find(episode) == -1:
        return "S00E00"

    while True:
        seasonNumber = seasonNumber + 1
        episodeNumber = 0
        while True:
            episodeNumber = episodeNumber + 1
            e = eN
            if len(str(episodeNumber)) == 1:
                eN = "0" + str(episodeNumber)
            else:
                eN = str(episodeNumber)

            if len(str(seasonNumber)) == 1:
                sN = "0" + str(seasonNumber)
            else:
                sN = str(seasonNumber)

            episode = "S" + sN + "E" + eN          

            if r.text.find(episode) == -1:
                break
        
        if episodeNumber == 1:
            seasonNumber = seasonNumber - 1
            if len(str(seasonNumber)) == 1:
                sN = "0" + str(seasonNumber)
            else:
                sN = str(seasonNumber)
            eN = int(e) - 1
            if len(str(eN)) == 1:
                eN = "0" + str(eN)
            else:
                eN = str(eN)
      
            break

    return "S" + sN + "E" + eN

if __name__ == "__main__":
    main()
