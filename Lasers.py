from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
#from matplotlib import pyplot as plt
import time
import math
import sys

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

# def VerticalLine(device, axis, travelmax, travelmin, numLines,f):
#     #Vertical lines
#     print("Vertical Lines", file=f)
#     loopcount = 0
#     while loopcount < numLines:
#         device.MOV(axis, travelmax)
#         WaitForMotionDone(device, int(axis))
#         device.MOV(axis, travelmin)
#         WaitForMotionDone(device, int(axis))
#         loopcount +=1
#     device.MOV(axis, 0)
#     WaitForMotionDone(device, int(axis))
    
def HorizontalLine(device, axis, travelmax, travelmin, numLines,f):
    #Horizontal lines
    print("Horizontal Lines", file=f)
    loopcount = 0
    while loopcount < numLines:
        device.MOV(axis, travelmax)
        WaitForMotionDone(device, int(axis))
        device.MOV(axis, travelmin)
        WaitForMotionDone(device, int(axis))
        loopcount +=1
    device.MOV(axis, 0)
    WaitForMotionDone(device, int(axis))
    
def PositiveDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines,f):
    #Positive Diagonal lines
    print("Positive Diagonal Lines", file=f)
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
        
def NegativeDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines,f):
    #Negative Diagonal lines
    print("Negative Diagonal Lines", file=f)
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
    
def Triangle(device, travelmax, numShapes,f):
    #Triangle
    print("Triangle", file=f)
    Polygon(device, 3, travelmax, numShapes)
    
def Diamond(device, travelmax, numShapes,f):
    #Diamond
    print("Diamond", file=f)
    Polygon(device, 4, travelmax, numShapes)
    
def Square(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numShapes,f):
    #Square
    print("Square", file=f)
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
        
def Pentagon(device, travelmax, numShapes,f):
    #Pentagon
    print("Pentagon", file=f)
    Polygon(device, 5, travelmax, numShapes)
    
def Hexagon(device, travelmax, numShapes,f):
    #Hexagon
    print("Hexagon", file=f)
    Polygon(device, 6, travelmax, numShapes)
    
# def Circle(device, travelmax, numShapes,f):
#     #Circle
#     print("Circle", file=f)
#     Polygon(device, 20, travelmax, numShapes)
    
def VerticalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans,f):
    #Vertical Raster Scan
    print("Vertical Raster Scan", file=f)
    print("Axis 1 Scanning, Axis 2 Stepping", file=f)
    loopcount = 0
    while loopcount < numScans:
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        for row in range(int(travelmin2), int(travelmax2), 1):
            if row % 2 == 0:
                device.MOV(axis1, travelmax1)
                #WaitForMotionDone(device, int(axis1))
                device.MOV(axis2, row + 1)
                #WaitForMotionDone(device, int(axis2))
            if row % 2 == 1:
                device.MOV(axis1, travelmin1)
                #WaitForMotionDone(device, int(axis1))
                device.MOV(axis2, row + 1)
                #WaitForMotionDone(device, int(axis2))
        loopcount +=1

def HorizontalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans,f):
    #Horizontal Linear Raster Scan
    print("Horizontal Raster Scan", file=f)
    print("Axis 1 Stepping, Axis 2 Scanning", file=f)
    loopcount = 0
    while loopcount < numScans:
        device.MOV(axis1, travelmin1)
        device.MOV(axis2, travelmin2)
        WaitForMotionDone(device, int(axis1))
        WaitForMotionDone(device, int(axis2))
        for row in range(int(travelmin1), int(travelmax1), 1):
            if row % 2 == 0:
                device.MOV(axis2, travelmax2)
                #WaitForMotionDone(device, int(axis2))
                device.MOV(axis1, row + 1)
                #WaitForMotionDone(device, int(axis1))
            if row % 2 == 1:
                device.MOV(axis2, travelmin2)
                #WaitForMotionDone(device, int(axis2))
                device.MOV(axis1, row + 1)
                #WaitForMotionDone(device, int(axis1))
        loopcount +=1
        
# def ConstVelCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles,f):
#     #Constant Velocity Concentric Circle Scan 
#     print("Constant Velocity Concentric Circle Scan", file=f)
#     outerloopcount = 0
#     loopcount = 0
#     while outerloopcount < numScans:
#         device.VEL(axis1, (500/numScans)*(outerloopcount+1))
#         device.VEL(axis2, (500/numScans)*(outerloopcount+1))
#         while loopcount < numCircles:
#             Polygon(device, 20, (loopcount+1)*(1/numCircles)*travelmax1, 1)
#             loopcount +=1
#         loopcount = 0
#         outerloopcount += 1
#         
# def ConstFreqCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles,f):
#     #Constant Frequency Concentric Circle Scan 
#     print("Constant Frequency Concentric Circle Scan", file=f)
#     outerloopcount = 0
#     loopcount = 0
#     while outerloopcount < numScans:
#         while loopcount < numCircles:
#             distance = (loopcount+1)*(2/numCircles)*travelmax1*3.14159
#             speed = int(distance / 2)
#             device.VEL(axis1, speed)
#             device.VEL(axis2, speed)
#             Polygon(device, 20, (loopcount+1)*(1/numCircles)*travelmax1, 1)
#             loopcount +=1
#         loopcount = 0
#         outerloopcount +=1
            
def ConstVelSpiral(device, axis1, axis2, travelmax1, numScans,f):
    #Constant Velocity Spiral Scan
    print("Constant Velocity Spiral Scan", file=f)
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
    
def Center(device, f):
    print("Centering", file=f)
    f.flush()
    device.MOV(['1','2'],[0,0])
    WaitForMotionDone(device, 1)
    WaitForMotionDone(device, 2)
    
def StartController(f):
    gateway = PISerial("/dev/ttyUSB0", 115200)
    messages = GCSMessages(gateway)
    v931 = GCSCommands(gcsmessage = messages)
    v931.RBT()
    time.sleep(15)
    gateway = PISerial("/dev/ttyUSB0", 115200)
    messages = GCSMessages(gateway)
    v931 = GCSCommands(gcsmessage = messages)
    #v931.WGO('1',0)
    #v931.WGO('2',0)
    v931.SVO('1',1)
    v931.SVO('2',1)
    v931.RON('1',1)
    v931.RON('2',1)
    print("Axis 1 Referencing", file=f)
    f.flush()
    v931.FRF(1)
    time.sleep(15)
    print("Axis 1 Referencing complete", file=f)
    f.flush()
    print("Axis 2 Referencing", file=f)
    f.flush()
    v931.FRF(2)
    time.sleep(15)
    print("Axis 2 Referencing complete", file=f)
    f.flush()
    Center(v931,f)
    v931.CCL(1,"ADVANCED")
    v931.SPA(1,100728832, 5000)#crank prof gen max vel limit
    v931.SPA(1,100729856, 5000)#crank prof gen max acc limit
    v931.SPA(1,100729600,0)#toggling profile gen on/off
    v931.SPA(2,100728832, 5000)#crank prof gen max vel limit
    v931.SPA(2,100729856, 5000)#crank prof gen max acc limit
    v931.SPA(2,100729600,0)#toggling profile gen on/off
    return v931
                
def GetTravel(device, f):
    travelmax1 = device.qTMX('1')['1'] - 5
    travelmin1 = device.qTMN('1')['1'] + 5
    print("{} {}".format(travelmax1, travelmin1), file=f)
    travelmax2 = device.qTMX('2')['2'] - 5
    travelmin2 = device.qTMN('2')['2'] + 5
    print("{} {}".format(travelmax2, travelmin2), file=f)
    return travelmax1, travelmin1, travelmax2, travelmin2

# def MakeWave(device, axis, travelmin, travelmax, f, iId, WaveTableID):
#     print("Make Wave", file=f)
#     
#     #configuration info
#     wgConfigiId = iId       # id of wave generator
#     wgConfigiWaveTableID = WaveTableID      # id of wave table
#     wgConfigiStartMode = 1       # start mode = 1 (start wave generator output synchronized by servo cycle)
#     wgConfigiNumCycles = 1000      # number of wave generator cycles, 0 = nonestopping
#     wgConfigdOffsetOfWave = 0     # offset of wave
#     wgConfigifrequencyOfWave = 43      # frequency of wave
#     wgConfigiInterpolationType = 0      # interpolation between points, used if piTableRate > 1. 1 = linear interpolation
#     wgConfigiOffsetOfFirstPointInWaveTable = 1      # index of starting point of curve in segment
#     wgConfigiAddAppendWave = "X"      # 0=clear wave table (1=add wavetable values, 2=append to existing wave table contents)
#     wgConfigbE727 = False  # false, if you are not using an E-727 Contro
#     wgConfigiTableRate = 1
#     #calculate amplitude
#     #travelmin1 = PIdevice.qTMN (axis)
#     #travelmax1 = PIdevice.qTMX (axis)
#     dAmplitudeOfWave = (abs(travelmin) + abs(travelmax))/2
#     
#     #query servo cycle time
#     PARAM_ServoUpdateTime = 234881536
#     servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
#     print("servo cycle time")
#     print(servoCycleTime)
#     print("servo cycle time")
#     
#     #calculate number of point in wavetable from given frequency
#     iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
#     #wavetable contains one segment
#     iSegmentLength = iNumberOfPoints
#     # curve center point is the middle of the segment
#     iCenterPointOfWave = int(iNumberOfPoints / 2)
#     #send wave table to controller
#     print(wgConfigiWaveTableID,wgConfigiOffsetOfFirstPointInWaveTable,iNumberOfPoints,wgConfigiAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLength)
#     device.WAV_SIN_P(wgConfigiWaveTableID,wgConfigiOffsetOfFirstPointInWaveTable,iNumberOfPoints,wgConfigiAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLength)
#     print("qwav")
#     print(device.qWAV())
#     #link wave table to wave generator
#     device.WSL(wgConfigiId, wgConfigiWaveTableID)
#     print("qwsl")
#     print(device.qWSL([1,2]))
#     # set wave table rate
#     device.WTR (wgConfigiId, wgConfigiTableRate, wgConfigiInterpolationType)
#     # set wave generator output cycles
#     device.WGC(wgConfigiId, wgConfigiNumCycles)
#     print('Move to start position',file=f)
#     # move to start position of sine-waveform
#     # !! Adjust start-position when changing waveform or assignment !!
#     device.MOV(axis, wgConfigdOffsetOfWave)
#     # wait for motion to stop
#     time.sleep(1)
#     
#     # restart recording as soon as wave generator output starts running
#     #PIdevice.WGR ();

def MakeWaves(device):
    wgConfigifrequencyOfWave = 20      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    iCenterPointOfWave = int(iNumberOfPoints / 2)
    
    
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLeng
    
    device.WAV_SIN_P(1,int(0.5*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #cos wave
    device.WAV_SIN_P(2,int(0.75*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #sin wave
    device.WAV_SIN_P(3,int(0*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #-cos wave
    device.WAV_SIN_P(4,int(0.25*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #-sin wave
    #device.WAV_SIN_P(2,1,300,'X',225, 60, -30,300) #sin Wave
    #device.WAV_SIN_P(3,1,300,'X',0, 60, -30,300) #-cos wave
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    #device.WTR(3,1,0)
    device.WGC(1,0)
    device.WGC(2,0)
    #device.WGC(3,1000)

def Line(device, axis, tableid, f):
    # start wave generator output, data recorder starts simultaneously
    print('Start wavegenerator',file=f)
    device.WSL(axis, tableid)
    #print(device.qGWD())
    if len(axis) == 1:
        device.WGO(axis, 1)
    else: device.WGO(axis, [1,1])
#     print("qwgo")
#     print(device.qWGO(axis))
#     print("qGWDaxis1")
#     print(device.qGWD(1,1,114))
#     print("qGWDaxis2")
#     print(device.qGWD(2,1,114))
    
    time.sleep(15)
#     device.WGO(axis,0)
    # wait for Wave Generator to finish
#     ret = True
#     while (ret == True):
#         #ret = device.IsGeneratorRunning(axis)
#         time.sleep(0.1);
    print('done', file=f)
    if len(axis) == 1:
        device.WGO(axis, 0)
    else: device.WGO(axis, [0,0])
    
def Driver():
    f = open('logfile.txt', 'w') 
    time.sleep(10)
    device = StartController(f)
    travelmax1, travelmin1, travelmax2, travelmin2 = GetTravel(device,f)
    numLines = 1
    numShapes = 1
    numScans = 1
    numCircles = 1
    axis1 = '1'
    axis2 = '2'
    cos = 1
    sin = 2
    ncos = 3
    nsin = 4
    device.VEL(axis1, (5000))
    device.VEL(axis2, (5000))
    #device.ACC(axis1, (5000))
    #device.ACC(axis2, (5000))
    #MakeWave(device, axis1, travelmin1, travelmax1, f, 1, 1)
    #MakeWave(device, axis2, travelmin2, travelmax2, f, 2, 2)
    #MakeWave(device, axis2, travelmin1, travelmax1, f, 2, 2)
    MakeWaves(device)
    f.close()
    while True:
        f = open('logfile.txt', 'a')
        start = time.time()
#        Circle(device, axis, numCircles, f)
        Center(device,f)
        Line(device, axis1, sin, f) #vertical line
        Center(device,f)
        Line(device, axis2, sin, f) #horizontal line
        Center(device,f)
        Line(device, [int(axis1), int(axis2)], [sin, sin],f) #postive line
        Center(device,f)
        Line(device, [int(axis1), int(axis2)], [sin, nsin],f) #Negative line
        Center(device,f)
        Line(device, [int(axis1), int(axis2)], [cos, sin],f) #circle
#         Center(device,f)
#         HorizontalLine(device, axis2, travelmax2, travelmin2, numLines,f)
#         Center(device,f)
#         PositiveDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines,f)
#         Center(device,f)
#         NegativeDiagonalLine(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numLines,f)
#         Center(device,f)
#         Triangle(device, travelmax1, numShapes,f)
#         Center(device,f)
#         Diamond(device, travelmax1, numShapes,f)
#         Center(device,f)
#         Square(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numShapes,f)
#         Center(device,f)
#         Pentagon(device, travelmax1, numShapes,f)
#         Center(device,f)
#         Hexagon(device, travelmax1, numShapes,f)
#         Center(device,f)
#         Circle(device, travelmax1, numShapes,f)
#         Center(device,f)
#         VerticalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans,f)
#         Center(device,f)
#         HorizontalRaster(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans,f)
#         Center(device,f)
#         #ConstVelCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles,f)
#         #Center(device,f)
#         #ConstFreqCircle(device, axis1, axis2, travelmax1, travelmin1, travelmax2, travelmin2, numScans, numCircles,f)
#         #Center(device,f)
#         ConstVelSpiral(device, axis1, axis2, travelmax1, numScans,f)
#         Center(device,f)
        end = time.time()
        print(end-start)
        f.close()

if __name__ == '__main__':
    Driver()
