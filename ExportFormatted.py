import csv
import pathfinding

maximizefuelefficiency = True

p = pathfinding.Pathfinder()

time = 0.0
vel = 100.0
thrust = 500.0
alt = 200.0

def makemove(i):
    global time
    
    s = decidemove(i)
    if(len(p.path[i]) == 2):
        time += 283.0/vel
    else:
        time += 200.0/vel
    return s
    
def decidemove(i):
    global maximizefuelefficiency
    global fuelmoves
    global limitspeedmoves
    if(maximizefuelefficiency):
        if(i < len(limitfuelmoves)):
            return limitfuelmoves[i]()
        else:
            j = i-len(limitfuelmoves)
            return fuelmoves[j % len(fuelmoves)]()
    else:
        if(i < 2):
            return maxaccel()
        elif(i == 2):
            return accel()
        else:
            return cruise()
    
def cruise():
    global thrust
    thrust -= 1.0
    return "CRUISE"
    
def maxaccel():
    global thrust
    global vel
    thrust -= 2.0
    vel += 40.0
    return "MAX-ACCELERATE"
    
def accel():
    global thrust
    global vel
    thrust -= 1.5
    vel += 20.0
    return "ACCELERATE"
    
def climb():
    global thrust
    global vel
    global alt
    thrust -= 2.0
    vel += 20.0
    alt += 20.0
    return "CLIMB"
    
def steepclimb():
    global thrust
    global alt
    thrust -= 2.0
    alt += 40.0
    return "STEEP-CLIMB"
    
def glide():
    global vel
    global alt
    vel -= 5.0
    alt -= 20.0
    return "GLIDE"
    
def cglide():
    global thrust
    global vel
    global alt
    thrust -= 0.5
    vel -= 5.0
    alt -= 10.0
    return "GLIDE-CRUISE"
    
fuelmoves = [climb, steepclimb, glide, glide, cglide, cglide]
limitspeedmoves = [maxaccel, climb, glide, maxaccel]
limitfuelmoves = [steepclimb, glide, glide, steepclimb, glide, glide, steepclimb, glide, glide]

if __name__ == "__main__":
    thefile = open('solution.csv', 'w', newline='')
    writer = csv.writer(thefile)
    
    header = ["Starting Location", "Starting Altitude(ft)", "Starting Velocity(fps)", "Starting Elapsed Time(s)", "Starting Thrust Points", "Move Type", "Move Direction", "Ending Location", "Ending Altitude(ft)", "Ending Velocity(fps)", "Ending Elapsed Time(s)", "Ending Thrust Points"]
    writer.writerow(header)
    
    p.setGraph([[['B','G'],[3,9]],[['H','AB'],[3,15]]])
    p.setStartLocation(pathfinding.Pos("AA", 10))
    p.shortestPathfind()
    p.visited = [pathfinding.Pos("AA", 10)] + p.visited
    #print("Path to fly:", p.path)
    #print("Visited Locales:", p.visited)
    
    #print(len(p.path))
    #print(len(p.visited))
    
    gofor = len(p.path)
    for i in range(0, gofor):
        stlocstring = pathfinding.Pos.convertDigitToAlphabetical(p.visited[i].xcord) + str(p.visited[i].ycord)
        #print(locstring)
        stalt = alt
        stvel = vel
        sttime = time
        stthrust = thrust
        m = makemove(i)
        elocstring = pathfinding.Pos.convertDigitToAlphabetical(p.visited[i+1].xcord) + str(p.visited[i+1].ycord)
        ealt = alt
        evel = vel
        etime = time
        ethrust = thrust
        writy = [stlocstring, stalt, stvel, sttime, stthrust, m, p.path[i], elocstring, ealt, evel, etime, ethrust]
        writer.writerow(writy)
        print(writy)