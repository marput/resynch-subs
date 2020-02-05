import re
import sys
import time
import math

class Srt():
    searchBefore = r"\d*\:\d*\:\d*\,\d*(?= )"
    searchAfter = r"(?<=\>.)\d*\:\d*\:\d*\,\d*"
    splitters = r":|,"

    def convertSecondsToTime(self, seconds):
        hours = int(seconds)//int(3600)
        seconds-=hours*3600
        minutes = int(seconds)//int(60)
        seconds-=minutes*60
        result = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        return result

    def moveTime(self, timeString, offset):
        splitTime = re.split(self.splitters, timeString)
        reversedSplitTime = list(reversed(splitTime))
        sum = 0
        miliseconds = reversedSplitTime[0]
        for i in range(1, len(reversedSplitTime)):
            sum+=int(reversedSplitTime[i])*pow(60, i-1)
        sum+=offset
        newTime = self.convertSecondsToTime(sum) + "," + str(miliseconds)
        return newTime

    def moveSubtitles(self, rawfile, subfile):
        for element in rawfile:
            match = re.search(self.searchBefore, element)
            if match:
                firstPart = self.moveTime(match[0], offset)
                match = re.search(self.searchAfter, element)
                secondPart = self.moveTime(match[0], offset)
                fullLine = firstPart + " --> " + secondPart + '\n'
                subfile.write(fullLine)
            else:
                subfile.write(element)
        rawfile.close()
        subfile.close()

class Ass:
    search_time = r"\d.*:\d*.\d*"

    def convertSecondsToTime(self, seconds):
        hours = int(seconds)//int(3600)
        seconds-=hours*3600
        minutes = int(seconds)//int(60)
        seconds-=minutes*60
        seconds = round(seconds, 2)
        result = str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        return result

    def moveTime(self, timeString, offset):
        splitTime = re.split(':', timeString)
        reversedSplitTime = list(reversed(splitTime)) #reverse the order from H:M:S to S:M:H
        sum = 0
        miliseconds = reversedSplitTime[0]
        for i in range(0, len(reversedSplitTime)):
            sum+=float(reversedSplitTime[i])*pow(60, i) #with reversed order, multiplying by i will yield correct conversion into seconds
        sum+=offset
        newTime = self.convertSecondsToTime(sum) 
        return newTime

    def moveSubtitles(self, rawfile, subfile):
        for element in rawfile:
            split_line = element.split(',')
            if re.search("Dialogue:", element): #if line has dialogue
                beginning = split_line[1]
                ending = split_line[2]
                beginning = self.moveTime(beginning, offset)
                ending = self.moveTime(ending, offset)
                del split_line[1:3]
                split_line.insert(1, beginning)
                split_line.insert(2, ending)
                result_line = ""
                for part in split_line:
                    result_line+=part + ","
                result_line = result_line[0:-1] #remove the trailing comma
                subfile.write(result_line)
            else:
                subfile.write(element)
        rawfile.close()
        subfile.close()

def getOffset(message):
    while True:
        offset = input(message)
        try:
            int(offset)
            return int(offset)
        except:
            print("Wrong input, try again.\n")

offset = getOffset("Enter the offset in seconds: ")


try:
    rawfile = open(sys.argv[1], "r")
except IndexError:
    print("Subtitle file hasn't been supplied, terminating...")
    sys.exit()
except FileNotFoundError:
    print("Subtitle file doesn't exist, terminating...")
    sys.exit()

if '.srt' in sys.argv[1]:
    extension = '.srt'
    try:
        subfile = open(sys.argv[2], "w")
    except IndexError:
        subfile = open("a" + extension, "w")
    srt = Srt()
    srt.moveSubtitles(rawfile, subfile)
elif '.ass' in sys.argv[1]:
    extension = '.ass'
    try:
        subfile = open(sys.argv[2], "w")
    except IndexError:
        subfile = open("a" + extension, "w")
    ass = Ass()
    ass.moveSubtitles(rawfile, subfile)
else:
    print("Subtitles are not in supported format, terminating...")
    rawfile.close()
    subfile.close()
        
            
    
