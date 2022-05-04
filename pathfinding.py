
# Graoh class created and written by Bridget Whitacre (^▽^), heavily edited by Sylvia Krech (=-=)
    #In general, I've taken Bridget's code, and compacted it via list comprehensions, and logic that doesnt involve using "theAlphabet"

# box formating [[['B','G'],[3,9]],[['H','AB'],[3,15]]]
class Graph:
    def __init__(self):
        self.graph = None
        self.flatGraph = None

    def main(self, boxDimentions):
        returnList = []
        for i in boxDimentions:
            xList, yList = i[0], i[1]
            startx, endx = Pos.convertAlphabeticalToInt(xList[0]), Pos.convertAlphabeticalToInt(xList[1])
            starty, endy = yList[0], yList[1]
            xaxis, yaxis = Graph.axisListGenerator(startx,endx), Graph.axisListGenerator(starty,endy)
            returnList.append([Pos(x,y) for x in xaxis for y in yaxis ])
        self.graph = returnList
        self.flatGraph = Graph.flatten(self.graph)
        return self.graph #for debug

    def axisListGenerator(start, end):
        return [i for i in range(start, end +1) ]

    # https://discourse.mcneel.com/t/python-flatten-an-irregular-list-of-list-of-list/4398/3
    # converts a list of arbirtrary dimensions into 1 dimensions.
    def flatten(lst):
        return sum( ([x] if not isinstance(x, list) else Graph.flatten(x) for x in lst), [] )

    def doesCellExist(self, pos):
        return pos in self.flatGraph

# Everything below written by Sylvia Krech
class Pathfinder:
    def __init__(self):
        self.graph = Graph()
        self.start = None
        self.currentPos = None
        # List of tuples defining which cells have been visited
        self.visited = [] # Do not mark the starting location as visited until end
        self.path = [] # List of directions to move 1 cell (i.e. a length of 5 North moves would be ["N","N","N","N","N"])
        self.lastMove = None
        self.ongoingDirection = None
        self.scanlineDescentDirection = None
        self.lastScanlineDirection = None

    def setGraph(self, input):
        self.graph.main(input)

    def setStartLocation(self, pos):
        self.start = pos
        self.currentPos = pos


    def shortestPathfind(self):
        print("Total number of squares to cover:", len(self.graph.flatGraph))
        xposint = self.start.xcord
        # find nearest wall
        closest = self.findWalls()
        print("closest", closest)
        self.move(closest[0])
        # will be against a wall
        self.moveFurthest()
        #will be in a corner
        self.scanlineDescentDirection = Pathfinder.oppositeDirection(self.path[-1])
        print("scanlineDirection", self.scanlineDescentDirection)
        self.moveFurthest() #move to furthestCorner
        self.updateLastScanlineDirection()
        # decend until we're about to be level with the start
        justSquarewaved = False
        while self.distAboveStart() > 1:
            if not justSquarewaved:
                self.gotoNewScanline()
            else:
                justSquarewaved = False
            self.moveFurthest(self.oppLastScanlineDirection)
            self.updateLastScanlineDirection()
            print("Distance to bottom:", self.disToWallInDir(self.scanlineDescentDirection))
            print(self.disToWallInDir(self.oppLastScanlineDirection))
            if self.disToWallInDir(self.scanlineDescentDirection) == 2:
                self.squareWaveMovement(self.scanlineDescentDirection, self.oppLastScanlineDirection)
                justSquarewaved = True

        # decend avoiding blocking the bit close to the starting wall + the start
        print("!!!!!!!!!!!!!!!!!!!!")
        self.updateLastScanlineDirection()
        self.gotoNewScanline()
        distToStartTile = self.currentDistanceFromStart() - 1
        print("distToStartTile", distToStartTile)
        self.move(Movement(self.oppLastScanlineDirection, distToStartTile))
        self.updateLastScanlineDirection()
        while self.disToWallInDir(self.scanlineDescentDirection) > 2:
            self.gotoNewScanline()
            print("Last oppLastScanlineDirection", self.oppLastScanlineDirection)
            print("Last lastScanlineDirection", self.lastScanlineDirection)
            self.move(Movement(self.oppLastScanlineDirection, distToStartTile))
            self.updateLastScanlineDirection()

        #close to the end, just finish it off
        #Okay so, if we get this far, we can either simply scanline to zip to the corner and head towards the end
        if self.disToWallInDir(self.scanlineDescentDirection) == 1:
            self.completeNewScanline()
        else: #Otherwise. Its a pain.
            self.squareWaveMovement(self.scanlineDescentDirection, self.oppLastScanlineDirection, distToStartTile)
            self.completeNewScanline()

        # Now we are in the corner opposite the furthest corner. we just have to get back
                #and now the most painful bit
                # very jank.
        self.scanlineDescentDirection = Pathfinder.oppositeDirection(self.scanlineDescentDirection)
        justSquarewaved = False
        while self.distAboveStart() > 1:
            self.completeNewScanline()
        self.moveFurthest(self.oppLastScanlineDirection) #cheat TODO make not a cheat

        #now compute shortestPathBack
        print("Computing shortestPathBack")
        while self.currentPos != self.start:
            print("hey!!!!")
            dir1 = "N" if self.currentPos.ycord > self.start.ycord else ("S" if self.currentPos.ycord < self.start.ycord else "")
            dir2 = "W" if self.currentPos.xcord > self.start.xcord else ("E" if self.currentPos.xcord < self.start.xcord else "")
            print("dir to move", dir1+dir2)
            self.move(Movement(dir1+dir2, 1))

        return self.verifySolution()

    def currentDistanceFromStart(self):
        return self.currentPos.distance(self.start)

    def completeNewScanline(self):
        self.gotoNewScanline()
        self.moveFurthest(self.oppLastScanlineDirection)
        self.updateLastScanlineDirection()

    def gotoNewScanline(self):
        self.move(Movement(self.scanlineDescentDirection, 1))

    def updateLastScanlineDirection(self):
        self.lastScanlineDirection = self.path[-1]
        self.oppLastScanlineDirection = Pathfinder.oppositeDirection(self.lastScanlineDirection)

    def squareWaveMovement(self, initialDirection, scanDirection, dis = 99999, initDescent = True):
        counter = 0
        print("Begining squareWaveMovement")
        if initDescent:
            self.move(Movement(initialDirection, 1))
        while self.disToWallInDir(self.scanlineDescentDirection) <= 2 and counter < dis:
            self.__squareWave(initialDirection,scanDirection)
            print("Distance to end of squareWaveMovement", self.disToWallInDir(scanDirection))
            counter += 2
        print("Ending squareWaveMovement")

    def __squareWave(self, initialDirection, scanDirection):
        print("Starting __squareWave at", self.currentPos)
        upDirection = Pathfinder.oppositeDirection(initialDirection)
        self.move(Movement(initialDirection, 1))
        self.move(Movement(scanDirection, 1))
        self.move(Movement(upDirection, 1))
        self.move(Movement(scanDirection, 1))

    # Computes furthest wall, and then runs into it, without going backwards
    # If given a movement, will move as far as it can that way?
    def moveFurthest(self, dir = None):
        if dir is None:
            farthest = self.findWalls(farthest=True)
        else:
            farthest = [Movement(dir, self.disToWallInDir(dir))]
        #print("Last dir", self.lastMove.dir)
        #print(farthest[0])
        if farthest[0].dir != Pathfinder.oppositeDirection(self.lastMove.dir) or dir is not None: #if furthest direction is not backwards
            self.move(farthest[0])
        else:
            self.move(farthest[1])

    def move(self, mov, saftey = True):
        self.lastMove = mov
        print("Moving", mov.dir)
        xmod = 1 if "E" in mov.dir else (-1 if "W" in mov.dir else 0)
        ymod = 1 if "S" in mov.dir else (-1 if "N" in mov.dir else 0)

        for i in range(mov.dis):
            self.currentPos = Pos((self.currentPos.xcord + xmod), (self.currentPos.ycord + ymod))
            if self.currentPos in self.visited:
                if saftey == True:
                    break # stop before covering unnessecaryTiles
                else:
                    print("uhoh! We're covering the same tile twice at,", self.currentPos)
            if not self.graph.doesCellExist(self.currentPos):
                if saftey == True:
                    break # stop before covering unnessecaryTiles
                else:
                    print("uhoh! we're going out of bounds of the nessecary space. I hope this is needed")
            self.visited.append(self.currentPos)
            self.path.append(mov.dir)
        print("Moved to", self.currentPos)

    # Find the walls along the cardinals from the given pos, returns a list of tuples in the form of (dir, dis)
        # by default it sorts to the nearest walls being first, and the farthest last, but putting fathest=True swaps that.
    def findWalls(self, farthest=False):
        output = []
        for i in ["N", "E", "S", "W"]:
            output.append(Movement(i, self.disToWallInDir(i)))
        print(output)
        output.sort(reverse=farthest, key=Pathfinder.sortByDistance)
        return output

    def disToWallInDir(self, dir, saftey=True):
        counter = 0
        xmod = 1 if "E" in dir else (-1 if "W" in dir else 0)
        ymod = 1 if "S" in dir else (-1 if "N" in dir else 0)
        while True:
            counter += 1
            cord = Pos((self.currentPos.xcord + (counter * xmod)), (self.currentPos.ycord + (counter * ymod)))
            if not self.graph.doesCellExist(cord) or (cord in self.visited and saftey):
                break
        return counter-1

    def sortByDistance(val):
        return val.dis

    #pls compact this if you know how
    def oppositeDirection(dir):
        output = ""
        if "N" in dir: output += "S"
        if "S" in dir: output += "N"
        if "W" in dir: output += "E"
        if "E" in dir: output += "W"
        return output

    #
    def distAboveStart(self):
        temp = -9999
        if self.scanlineDescentDirection == "N":
            temp = self.currentPos.ycord - self.start.ycord
        elif self.scanlineDescentDirection == "S":
            temp = self.start.ycord - self.currentPos.ycord
        elif self.scanlineDescentDirection == "E":
            temp = self.start.xcord - self.currentPos.xcord
        elif self.scanlineDescentDirection == "W":
            temp = self.currentPos.xcord - self.start.xcord
        print("aboveStart?", temp)
        return temp


    def verifySolution(self):
        counter = 0
        for cell in self.visited:
            if not self.graph.doesCellExist(cell):
                counter +=1

        counter2 = 0
        missedCells = []
        for cell in self.graph.flatGraph:
            if cell not in self.visited:
                counter2 +=1
                missedCells.append(cell)

        counter3 = 0
        for dir in self.path:
            if len(dir) > 1:
                counter3 += 1
        counter4 = len(self.path) - len(self.graph.flatGraph)
        flag = counter == 0 and counter2 == 0 and counter3 <= 1 and counter4 == 0
        if not flag:
            print("Flew for", len(self.path), "cells")
            print(self.visited)
            if counter != 0: print("Flew outside of required boundaries for", counter, "cells")
            if counter2 != 0:
                print("Not all cells visited,", counter2, "cells missed")
                print("Specifically,", missedCells)
            if counter3 > 1: print("More intercardinals than nessecary,", counter3, "intercardinals used total")
            if counter4 != 0: print("More movements than nessecary,", counter4)

        return flag

# classes entirely for holding data in a nicer way
class Movement:
    def __init__(self, dir, dis):
        if type(dir) == type(1) and type(dis) == type(""): #catch mishap
            print("Hey! you didnt init this properly. I'll fix it this time.")
            self.dir = dis
            self.dis = dir
        else:
            self.dir = dir
            self.dis = dis

    def __repr__(self):
        return "Mov: " + self.dir + " for " + str(self.dis) + " units"

class Pos:
    def __init__(self, xcord, ycord):
        self.ycord = ycord
        self.alphabeticx, self.xcord = xcord, xcord
        if type(xcord) == type(5):
            self.alphabeticx = Pos.convertDigitToAlphabetical(xcord)
        else:
            self.xcord = Pos.convertAlphabeticalToInt(xcord)

    # Converts a number to its corresponding alphabetic thing.
    # For example:
        # 1 => A, 26 => Z, 27 => AA, 702 => ZZ, 703 => AAA
    def convertDigitToAlphabetical(num):
        output = ""
        while num != 0: #okay, honestly, i have no idea why these -1s are in here. i dont want to know why. it works.
            output = chr(((num-1) % 26)+65) + output # convert ""directly"" to ascii
            num = (num-1) // 26
        return output

    # Inverse of the above
        #Hopefully, by the end of this rework should never be called
    def convertAlphabeticalToInt(alpha):
        output = 0
        while alpha != "":
            output *= 26 # move up a decimal place in base 26
            output += ord(alpha[0])-64 # convert directly from ascii
            alpha = alpha[1:]
        return output

    def distance(self, other):
        return abs(self.xcord - other.xcord) + abs(self.ycord - other.ycord)

    def __repr__(self):
        return "[" + self.alphabeticx + ", " + str(self.ycord) + "]"

    def __eq__(self, other):
        return self.xcord == other.xcord and self.ycord == other.ycord

    def __ne__(self, other):
        return not self == other

### CONVERSION + GRAPH TESTING
if False:
    tempGraph = Graph()
    print(tempGraph.main([[['B','G'],[3,9]],[['H','AB'],[3,15]]]))
    print( "If anything below this runs false, oh no.")
    print( "AAA" == Pos.convertDigitToAlphabetical(703), Pos.convertDigitToAlphabetical(703))
    print( "ZZ" == Pos.convertDigitToAlphabetical(702), Pos.convertDigitToAlphabetical(702))
    print( "AA" == Pos.convertDigitToAlphabetical(27), Pos.convertDigitToAlphabetical(27))
    print( "Z" == Pos.convertDigitToAlphabetical(26), Pos.convertDigitToAlphabetical(26))
    print( "A" == Pos.convertDigitToAlphabetical(1), Pos.convertDigitToAlphabetical(1))
    print( 1 == Pos.convertAlphabeticalToInt("A"))
    print( 26 == Pos.convertAlphabeticalToInt("Z"))
    print( 27 == Pos.convertAlphabeticalToInt("AA"))
    print( 703 == Pos.convertAlphabeticalToInt("AAA"))
    print( 728 == Pos.convertAlphabeticalToInt("AAZ"), Pos.convertAlphabeticalToInt("AAZ"))
### TESTING END

###PATHFINDER TESTING
if False:
    testing = [Pos(0,0)]
    test2 = Pos(0,0)
    print("Does Pos in a list work?", test2 in testing)
    a = Pathfinder()
    a.setGraph([[['B','G'],[3,9]],[['H','AB'],[3,15]]])
    a.setStartLocation(Pos("AA", 10))
    a.move(Movement("NE",1))
    print(a.path)
### TESTING END

### The actual goal
if __name__ == "__main__":

    pather = Pathfinder()
    pather.setGraph([[['B','G'],[3,9]],[['H','AB'],[3,15]]])
    pather.setStartLocation(Pos("AA", 10))
    pather.shortestPathfind()
    print("Path to fly:", pather.path)
