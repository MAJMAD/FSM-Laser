import math

def FindCirclePositions(n, r, x, y):
    """Find, print, and return a list of coordinates on a n-sided polygon/circle approximation.
    @param n : Number of points of a polygon, should be at least 3, the bigger the number, the better the circle approximation.
    @param r : Radius of the circle that is to be approximated.
    @param x : X coordinate of circle centerpoint/origin
    @param y : Y coordinate of circle centerpoint/origin
    """
    pi = 3.14159
    Xpos = [] # List of X coordinates on the circle approximation
    Ypos = [] # List of Y coordinates on the circle approximation
    for point in range(n):
        X = r * math.sin(2 * pi * point / n) + x
        Y = r * math.cos(2 * pi * point / n) + y
        Xpos.append(X)
        Ypos.append(Y)
    print(Xpos)
    print(Ypos)
    return Xpos, Ypos

def FindCircleVelocities(n, r, x, y, t):
    """Find, print, and return a list of x and y component travel distances, velocities, and the total velocity to realize a n-sided polygon/circle approximation.
    @param n : Number of points of a polygon, should be at least 3, the bigger the number, the better the circle approximation.
    @param r : Radius of the circle that is to be approximated.
    @param x : X coordinate of circle centerpoint/origin
    @param y : Y coordinate of circle centerpoint/origin
    @param t : Time to realize each motion segment, note total time to realize the circle approximation will be n * t
    """
    Xpos, Ypos = FindCirclePositions(n, r, x, y)
    Xdis = [] # List of X component displacements
    Ydis = [] # List of Y component displacements
    Xvel = [] # List of X component velocities
    Yvel = [] # List of Y component velocities
    Totalvel = [] # List of total velocities (should be constant)
    for point in range(n-1):
        Xdis.append(Xpos[point + 1] - Xpos[point])
        Ydis.append(Ypos[point + 1] - Ypos[point])
        Xvel.append(Xdis[point] / t)
        Yvel.append(Ydis[point] / t)
        Totalvel.append(math.sqrt(Xvel[point] ** 2 + Yvel[point] ** 2))
    print(Xdis)
    print(Ydis)
    print(Xvel)
    print(Yvel)
    print(Totalvel)
    return Xvel, Yvel

def FindGCSMacro(n, r, x, y, t):
    """Find the GCS Macro to realize a n-sided polygon/circle approximation.
    @param n : Number of points of a polygon, should be at least 3, the bigger the number, the better the circle approximation.
    @param r : Radius of the circle that is to be approximated.
    @param x : X coordinate of circle centerpoint/origin
    @param y : Y coordinate of circle centerpoint/origin
    @param t : Time to realize each motion segment, note total time to realize the circle approximation will be n * t"""
    Xpos, Ypos = FindCirclePositions(n, r, x, y)
    Xvel, Yvel = FindCircleVelocities(n, r, x, y, t)
    GCSXPositionCommands = [] # List of X axis position commands
    GCSYPositionCommands = [] # List of Y axis position commands
    GCSXVelocityCommands = [] # List of X axis velocity commands
    GCSYVelocityCommands = [] # List of Y axis velocity commands
    for position in range(len(Xpos)):
        GCSXPositionCommands.append("1 MOV 1 {}\n".format(Xpos[position]))
    for position in range(len(Ypos)):
        GCSYPositionCommands.append("2 MOV 1 {}\n".format(Ypos[position]))
    for velocity in range(len(Xvel)):
        GCSXVelocityCommands.append("1 VEL 1 {}\n".format(Xvel[velocity]))
    for velocity in range(len(Yvel)):
        GCSYVelocityCommands.append("2 VEL 1 {}\n".format(Yvel[velocity]))
    Macro = open('CircleMacro.txt', 'w')
    Macro.write("1 MOV 1 50\n")
    Macro.write("2 MOV 1 50\n")
    Macro.write("1 DFH 1\n")
    Macro.write("2 DFH 1\n")
    Macro.write("1 ACC 1 10\n")
    Macro.write("2 ACC 1 10\n")
    Macro.write(GCSXPositionCommands[0])
    Macro.write(GCSYPositionCommands[0])
    for motion in range(len(Xvel)):
        Macro.write(GCSXVelocityCommands[motion])
        Macro.write(GCSYVelocityCommands[motion])
        Macro.write(GCSXPositionCommands[motion+1])
        Macro.write(GCSYPositionCommands[motion+1])
        Macro.write("1 WAC ONT? 1 = 1\n")
        Macro.write("2 WAC ONT? 1 = 1\n")
    Macro.close()

if __name__ == '__main__':
    FindGCSMacro(20, 5, 0, 0, 1)