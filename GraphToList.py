# Created and Written by Bridget Whitacre (^▽^)
# box formating (((B,G),(3,9)),((H,AB),(3,15)))

#class GraphToList:

theAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 

def main(boxDimentions):
    returnList = []
    for i in boxDimentions:
        xList = i[0]
        yList = i[1]
        startx = xList[0]
        endx = xList[1]
        starty = yList[0]
        endy = yList[1]

    
def findAlphabetLocation(lookValue):
    counter = 0
    for i in theAlphabet:
        counter += 1
        if i == lookValue:
            return(counter)

def yAxisListGenerator(starty, endy):
    returnList = []
    counter = starty
    
    while (counter != endy + 1):
        returnList.append(counter)
        counter += 1

    return returnList

def xAxisListGenerator(startx, endx):
    letterToAdd = ''
    startVal = findAlphabetLocation(startx) - 1
    counter = 0
    returnList = []
    while(True):
        placeHold = counter + startVal
        
        if ((placeHold) >= len(theAlphabet)):
            if (letterToAdd == ''):
                letterToAdd = 'A'
                counter = 1
                startVal = 0
                returnList.append(letterToAdd + theAlphabet[0])
            else:
                for i in range(0,len(theAlphabet)):
                    if (theAlphabet[i] == letterToAdd):
                        counter = 1
                        letterToAdd = theAlphabet[i + 1] 
                        break
        
        elif (letterToAdd + theAlphabet[placeHold] == endx):
            returnList.append(letterToAdd + theAlphabet[placeHold])
            return(returnList)
        
        else:
            returnList.append(letterToAdd + theAlphabet[placeHold])
            counter += 1




print(xAxisListGenerator('B','AD'))