import glob
import re

mlpaf_season1Files = glob.glob("sources/My Little Pony 'n Friends - S01*.srt")
mlpaf_season2Files = glob.glob("sources/My Little Pony 'n Friends - S02*.srt")
mlpfim_season1Files = glob.glob("sources/MLPFIM.S01*.srt")

reNumber = re.compile(r"^\d+$")
reTimeStamp = re.compile(" --> ")
reSong = re.compile("â™ª")
reInParen = re.compile("\([^\)]+\)")
reEncodingFormat = re.compile("ï»¿1")


def is_number(trimmedString):
    s1 = ''.join(map(hex, bytearray(trimmedString, "UTF-8")))
    s2 = ''.join(map(hex, bytearray("1", "UTF-8")))
    trimmedStrin2 = '1'

    #print(str(s1[0]))
    #print(str(s2[0]))

    m = re.search(u"^\d+$", trimmedString)
    return m is not None


def is_encodingformat(trimmedString):
    m = reEncodingFormat.search(trimmedString)
    return m is not None


def is_timestamp(trimmedString):
    m = reTimeStamp.search(trimmedString)
    return m is not None


def is_song(trimmedString):
    m = reSong.search(trimmedString)
    return m is not None


def is_inparens(trimmedString):
    m = reInParen.search(trimmedString)
    return m is not None


def cleanString(line):
    goodline = line.encode("cp1252").decode('utf8')
    newLine = goodline.strip("- ")            # remove double speaker indication
    newLine = re.sub("<[^>]+>", '', newLine)  # remove italics
    newLine = re.sub("★☆★", '', newLine)   # remove emphasis
    newLine = re.sub("[^:]+:", '', newLine)   # remove speaker indication
    return newLine.strip() + "\n"

def getTextLine(line):
    if line == "":
        return None
    if is_number(line) or is_timestamp(line) or is_song(line) or is_inparens(line) or is_encodingformat(line):
        print("skipping: " + line)
        return None
    else:
        return cleanString(line + "\n")


def getText(fileName):
    text = ""
    file = open(fileName,encoding="cp1252")
    for line in file:
        trimmedLine = line.strip()
        tempText = getTextLine(trimmedLine)
        if tempText is not None and tempText.strip() != '':
            text += tempText
    file.close()
    return text


def iterateFiles(season, fileNames):
    outfile = open(season + "_dialog.txt","w",encoding="utf-8")
    for fileName in fileNames:
        print(fileName)
        text = getText(fileName)
        #print(text + "\n")
        outfile.write(text)
    outfile.close()


iterateFiles("mlpaf.s01", mlpaf_season1Files)

iterateFiles("mlpaf.s02", mlpaf_season2Files)

iterateFiles("mlpfim.s01", mlpfim_season1Files)

