## TODO
    # Implement pathfinding checker (to see if min length + if goes out of bounds/double covers)
    # Implement a second Graph that contains the illegal tiles.
        # And implement into checker + main pathfinding


# Created and Written by Bridget Whitacre (^▽^), heavily edited by Sylvia Krech (=-=)
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
            startx, endx = Graph.convertAlphabeticalToInt(xList[0]), Graph.convertAlphabeticalToInt(xList[1])
            starty, endy = yList[0], yList[1]
            xaxis, yaxis = Graph.xAxisListGenerator(startx,endx), Graph.yAxisListGenerator(starty,endy)
            returnList.append([(x,y) for x in xaxis for y in yaxis ]) #tuples so flatten doesnt flatten
        self.graph = returnList
        self.flatGraph = Graph.flatten(self.graph)
        return self.graph #for debug


    def yAxisListGenerator(starty, endy):
        return [i for i in range(starty, endy +1) ]

    def xAxisListGenerator(startx, endx, alphabetical = False):
        return [Graph.convertDigitToAlphabetical(i) for i in range(startx, endx+1)]

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
    def convertAlphabeticalToInt(alpha):
        output = 0
        while alpha != "":
            output *= 26 # move up a decimal place in base 26
            output += ord(alpha[0])-64 # convert directly from ascii
            alpha = alpha[1:]
        return output

    # https://discourse.mcneel.com/t/python-flatten-an-irregular-list-of-list-of-list/4398/3
    # converts a list of arbirtrary dimensions into 1 dimensions.
    def flatten(lst):
        return sum( ([x] if not isinstance(x, list) else Graph.flatten(x) for x in lst), [] )

    #pos is a list with an x and a y cord. X can be alphabetic already or not. idc. it checks.
    def doesCellExist(self, pos):
        tempPos = pos
        if type(tempPos[0]) != type(""):
            tempPos[0] = Graph.convertDigitToAlphabetical(tempPos[0])
        return tuple(tempPos) in self.flatGraph


### TESTING
tempGraph = Graph()
print(tempGraph.main([[['B','G'],[3,9]],[['H','AB'],[3,15]]]))
print( "If anything below this runs false, oh no.")
print( "AAA" == Graph.convertDigitToAlphabetical(703), Graph.convertDigitToAlphabetical(703))
print( "ZZ" == Graph.convertDigitToAlphabetical(702), Graph.convertDigitToAlphabetical(702))
print( "AA" == Graph.convertDigitToAlphabetical(27), Graph.convertDigitToAlphabetical(27))
print( "Z" == Graph.convertDigitToAlphabetical(26), Graph.convertDigitToAlphabetical(26))
print( "A" == Graph.convertDigitToAlphabetical(1), Graph.convertDigitToAlphabetical(1))
print( 1 == Graph.convertAlphabeticalToInt("A"))
print( 26 == Graph.convertAlphabeticalToInt("Z"))
print( 27 == Graph.convertAlphabeticalToInt("AA"))
print( 703 == Graph.convertAlphabeticalToInt("AAA"))
print( 728 == Graph.convertAlphabeticalToInt("AAZ"), Graph.convertAlphabeticalToInt("AAZ"))
### TESTING END

# Written by Sylvia Krech
class Pathfinder:
    def __init__(self):
        self.graph = Graph()
        self.start = None
        self.currentPos = None
        # List of tuples defining which cells have been visited
        self.visited = [] # Do not mark the starting location as visited until end
        # List of directions to move 1 cell (i.e. a length of 5 North moves would be ["N","N","N","N","N"])
        self.path = []
        self.lastDir= ""

    def setGraph(self, input):
        self.graph.main(input)

    def setStartLocation(self, location):
        self.start = location
        self.currentPos = location
        if type(self.currentPos[0]) == type(""):
            self.currentPos = (Graph.convertAlphabeticalToInt(self.currentPos[0]), self.currentPos[1])

    def shortestPathfind(self):
        print("Total number of squares to cover:", len(self.graph.flatGraph))
        pos = self.start
        xposint = Graph.convertAlphabeticalToInt(pos[0])
        counter = 0
        # find nearest wall
        closest = self.findWalls(self.start)
        print(closest)
        self.move(closest[0])
        # will be against a wall
        #while True:
        farthest = self.findWalls(self.start, farthest=True)
        if farthest[0] != Pathfinder.oppositeDirection(self.lastDir): #if furthest direction is not backwards
            self.move(farthest[0])
        else:
            self.move(farthest[1])

    def move(self, mov):
        self.lastMove = mov
        xmod = 1 if "E" in mov.dir else (-1 if "W" in mov.dir else 0)
        ymod = 1 if "S" in mov.dir else (-1 if "N" in mov.dir else 0)

        for i in range(mov.dis):
            self.currentPos = ((self.currentPos[0] + xmod), (self.currentPos[1] + ymod))
            if self.currentPos in self.visited:
                print("uhoh! We're covering the same tile twice at,", self.currentPos)
                #deal with it? maybe?
            if self.currentPos not in self.graph.flatGraph:
                print("uhoh! we're going out of bounds of the nessecary space. I hope this is needed")
            print("Moved to", self.currentPos)
            print("Moved to [", Graph.convertDigitToAlphabetical(self.currentPos[0]), self.currentPos[1], "]")
            self.visited.append(self.currentPos)


    # Find the walls along the cardinals from the given pos, returns a list of tuples in the form of (dir, dis)
        # by default it sorts to the nearest walls being first, and the farthest last, but putting fathest=True swaps that.
    def findWalls(self, pos, farthest=False):
        output = []
        for i in ["N", "E", "S", "W"]:
            output.append(Movement(i, self.disToWallInDir(pos, i)))
        print(output)
        output.sort(reverse=farthest, key=Pathfinder.sortSecond)
        return output

    def disToWallInDir(self, pos, dir):
        xcord = pos[0] if type(pos[0]) == type(0) else Graph.convertAlphabeticalToInt(pos[0])
        ycord = pos[1]
        counter = 0
        xmod = 1 if "E" in dir else (-1 if "W" in dir else 0)
        ymod = 1 if "S" in dir else (-1 if "N" in dir else 0)
        while True:
            counter += 1
            if not self.graph.doesCellExist([(xcord + (counter * xmod)), (ycord + (counter * ymod))]):
                break
        print(counter)
        return counter-1

    def sortSecond(val):
        return val.dis

    #pls compact this if you know how
    def oppositeDirection(dir):
        output = ""
        if "N" in dir: output += "S"
        if "S" in dir: output += "N"
        if "W" in dir: output += "E"
        if "E" in dir: output += "W"
        return output

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

pather = Pathfinder()
pather.setGraph([[['B','G'],[3,9]],[['H','AB'],[3,15]]])
pather.setStartLocation(["AA", 10])
pather.shortestPathfind()
 
