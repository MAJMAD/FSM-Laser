from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
from matplotlib import pyplot as plt
import time
import math

def WaitForMotionDone(device, axis):
    isMoving = True
    while isMoving:
        isMoving = device.IsMoving(axis)[axis]
        
def Polygon(device, n, r, loopval):
    pi = 3.14159
    Xpos = [] # List of X coordinates on the circle approximation
    Ypos = [] # List of Y coordinates on the circle approximation
    for point in range(n+1):
        X = r * math.sin(2 * pi * point / n)
        Y = r * math.cos(2 * pi * point / n)
        Xpos.append(X)
        Ypos.append(Y)
    loopcount = 0
    while loopcount < loopval:
        for point in range(n+1):
            device.MOV(['1', '2'], [Ypos[point], Xpos[point]])
            #device.MOV('2', Xpos[point])
            WaitForMotionDone(device, 1)
            WaitForMotionDone(device, 2)
        loopcount +=1
#     plt.plot(Xpos, Ypos, color='red')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.title('Generated Motion Profile')
#     plt.grid(True)
#     plt.show()
        
def Spiral(device, n, r, loopval):
    pi = 3.14159
    Xpos = [] # List of X coordinates on the circle approximation
    Ypos = [] # List of Y coordinates on the circle approximation
    for point in range(n):
        X = r * point / n * math.sin(2 * pi * point / n)
        Y = r * point / n * math.cos(2 * pi * point / n)
        Xpos.append(X)
        Ypos.append(Y)
    loopcount = 0
    while loopcount < loopval:
        for point in range(n):
            device.MOV('1', Xpos[point])
            device.MOV('2', Ypos[point])
            WaitForMotionDone(device, 1)
            WaitForMotionDone(device, 2)
        loopcount +=1

def VerticalLine(device, axis, travelmax, travelmin, numLines):
    #Vertical lines
    #print("Vertical Lines")
    loopcount = 0
    while loopcount < numLines:
        device.MOV(axis, travelmax)
        WaitForMotionDone(device, int(axis))
        device.MOV(axis, travelmin)
        WaitForMotionDone(device, int(axis))
        loopcount +=1
    device.MOV(axis, 0)
    WaitForMotionDone(device, int(axis))
    
def HorizontalLine(device, axis, travelmax, travelmin, numLines):
    #Horizontal lines
    #print("Horizontal Lines")
    loopcount = 0
    while loopcount < numLines:
        device.MOV(axis, travelmax)
        WaitForMotionDone(device, int(axis))
        device.MOV(axis, travelmin)
        WaitForMotionDone(device, int(axis))
        loopcount +=1
    device.MOV(axis, 0)
    WaitForMotionDone(device, int(axis))
    
def PositiveDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines):
    #Positive Diagonal lines
    #print("Positive Diagonal Lines")
    loopcount = 0
    while loopcount < numLines:
        device.MOV(axis1, travelmax1)
        device.MOV(axis2, travelmax2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        loopcount +=1
    device.MOV(axis1, 0)
    device.MOV(axis2, 0)
    WaitForMotionDone(device, int(axis1))
    WaitForMotionDone(device, int(axis2))
        
def NegativeDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines):
    #Negative Diagonal lines
    #print("Negative Diagonal Lines")
    loopcount = 0
    while loopcount < numLines:
        device.MOV(axis1, travelmax1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmax2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        loopcount +=1
    
def Triangle(device, travelmax, numShapes):
    #Triangle
    #print("Triangle")
    Polygon(device, 3, travelmax, numShapes)
    
def Diamond(device, travelmax, numShapes):
    #Diamond
    #print("Diamond")
    Polygon(device, 4, travelmax, numShapes)
    
def Square(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numShapes):
    #Square
    #print("Square")
    loopcount = 0
    while loopcount < numShapes:
        device.MOV(axis1, travelmax1)
        device.MOV(axis2, travelmax2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis2))
        device.MOV(axis1, travelmin1)
        WaitForMotionDone(device, int(axis1))
        device.MOV(axis2, travelmax2)
        WaitForMotionDone(device, int(axis2))
        device.MOV(axis1, travelmax1)
        WaitForMotionDone(device, int(axis1))
        loopcount += 1
        
def Pentagon(device, travelmax, numShapes):
    #Pentagon
    #print("Pentagon")
    Polygon(device, 5, travelmax, numShapes)
    
def Hexagon(device, travelmax, numShapes):
    #Hexagon
    #print("Hexagon")
    Polygon(device, 6, travelmax, numShapes)
    
def Circle(device, travelmax, numShapes):
    #Circle
    #print("Circle")
    Polygon(device, 20, travelmax, numShapes)
    
def VerticalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans):
    #Vertical Raster Scan
    #print("Vertical Raster Scan")
    #print("Axis 1 Scanning, Axis 2 Stepping")
    loopcount = 0
    while loopcount < numScans:
        device.VEL(axis1, (500/numScans)*(loopcount+1))
        device.VEL(axis2, (500/numScans)*(loopcount+1))
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        for row in range(int(travelmin2), int(travelmax2), 1):
            if row % 2 == 0:
                device.MOV(axis1, travelmax1)
                WaitForMotionDone(device, int(axis1))
                device.MOV(axis2, row + 1)
                WaitForMotionDone(device, int(axis2))
            if row % 2 == 1:
                device.MOV(axis1, travelmin1)
                WaitForMotionDone(device, int(axis1))
                device.MOV(axis2, row + 1)
                WaitForMotionDone(device, int(axis2))
        loopcount +=1

def HorizontalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans):
    #Horizontal Linear Raster Scan
    #print("Horizontal Raster Scan")
    #print("Axis 1 Stepping, Axis 2 Scanning")
    loopcount = 0
    while loopcount < numScans:
        device.VEL(axis1, (500/numScans)*(loopcount+1))
        device.VEL(axis2, (500/numScans)*(loopcount+1))
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        for row in range(int(travelmin1), int(travelmax1), 1):
            if row % 2 == 0:
                device.MOV(axis2, travelmax2)
                WaitForMotionDone(device, int(axis2))
                device.MOV(axis1, row + 1)
                WaitForMotionDone(device, int(axis1))
            if row % 2 == 1:
                device.MOV(axis2, travelmin2)
                WaitForMotionDone(device, int(axis2))
                device.MOV(axis1, row + 1)
                WaitForMotionDone(device, int(axis1))
        loopcount +=1
        
def ConstVelCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles):
    #Constant Velocity Concentric Circle Scan 
    #print("Constant Velocity Concentric Circle Scan")
    outerloopcount = 0
    loopcount = 0
    while outerloopcount < numScans:
        device.VEL(axis1, (500/numScans)*(outerloopcount+1))
        device.VEL(axis2, (500/numScans)*(outerloopcount+1))
        while loopcount < numCircles:
            Polygon(device, 20, (loopcount+1)*(1/numCircles)*travelmax1, 1)
            loopcount +=1
        loopcount = 0
        outerloopcount += 1
        
def ConstFreqCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles):
    #Constant Frequency Concentric Circle Scan 
    #print("Constant Frequency Concentric Circle Scan")
    outerloopcount = 0
    loopcount = 0
    while outerloopcount < numScans:
        while loopcount < numCircles:
            distance = (loopcount+1)*(2/numCircles)*travelmax1*3.14159
            speed = int(distance / 2)
            device.VEL(axis1, speed)
            device.VEL(axis2, speed)
            Polygon(device, 20, (loopcount+1)*(1/numCircles)*travelmax1, 1)
            loopcount +=1
        loopcount = 0
        outerloopcount +=1
            
def ConstVelSpiral(device, axis1, axis2, travelmax1, numScans):
    #Constant Velocity Spiral Scan
    limit = travelmax1/(numScans*2*3.14159)
    points = []
    xpos = []
    ypos = []
    for point in range(0, int(numScans*2*3.14159*100000), int(0.314159*100000)):
        points.append(point/100000)
    for point in range(0, len(points)):
        xpos.append(limit*points[point]*math.cos(points[point]))
        ypos.append(limit*points[point]*math.sin(points[point]))
    for point in range(0, len(points)):
        device.MOV([axis1, axis2],[xpos[point],ypos[point]])
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
    
def Center(device):
    #print("Centering")
    device.MOV(['1', '2'], [0,0])
    WaitForMotionDone(device, 1)
    WaitForMotionDone(device, 2)
    
def StartController():
    gateway = PISerial("/dev/ttyUSB0", 115200)
    messages = GCSMessages(gateway)
    v931 = GCSCommands(gcsmessage = messages)
    v931.SVO('1',1)
    v931.SVO('2',1)
    v931.RON('1',1)
    v931.RON('2',1)
    #print("Axis 1 Referencing")
    v931.FRF(1)
    referencing = False
    while not referencing:
        referencing = v931.IsControllerReady()
    #print("Axis 1 Referencing complete")
    #print("Axis 2 Referencing")
    v931.FRF(2)
    referencing = False
    while not referencing:
        referencing = v931.IsControllerReady()
    #print("Axis 2 Referencing complete")
    Center(v931)
    return v931
                
def GetTravel(device):
    travelmax1 = device.qTMX('1')['1'] - 5
    travelmin1 = device.qTMN('1')['1'] + 5
    #print("{} {}".format(travelmax1, travelmin1))
    travelmax2 = device.qTMX('2')['2'] - 5
    travelmin2 = device.qTMN('2')['2'] + 5
    #print("{} {}".format(travelmax2, travelmin2))
    return travelmax1, travelmin1, travelmax2, travelmin2

def Driver():
    device = StartController()
    travelmax1, travelmin1, travelmax2, travelmin2 = GetTravel(device)
    numLines = 1
    numShapes = 1
    numScans = 1
    numCircles = 1
    axis1 = '1'
    axis2 = '2'
    while True:
        VerticalLine(device, axis1, travelmax1, travelmin1, numLines)
        Center(device)
        HorizontalLine(device, axis2, travelmax2, travelmin2, numLines)
        Center(device)
        PositiveDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines)
        Center(device)
        NegativeDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines)
        Center(device)
        Triangle(device, travelmax1, numShapes)
        Center(device)
        Diamond(device, travelmax1, numShapes)
        Center(device)
        Square(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numShapes)
        Center(device)
        Pentagon(device, travelmax1, numShapes)
        Center(device)
        Hexagon(device, travelmax1, numShapes)
        Center(device)
        Circle(device, travelmax1, numShapes)
        Center(device)
        VerticalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans)
        Center(device)
        HorizontalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans)
        Center(device)
        ConstVelCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles)
        Center(device)
        ConstFreqCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles)
        Center(device)
        ConstVelSpiral(device, axis1, axis2, travelmax1, numScans)
        Center(device)

if __name__ == '__main__':
    Driver()