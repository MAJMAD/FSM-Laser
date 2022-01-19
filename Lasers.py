from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
import time
import math
import sys

def WaitForMotionDone(device, axis):
    isMoving = True
    while isMoving:
        isMoving = device.IsMoving(axis)[axis]
        
def Polygon(n, r, f):
    pi = 3.14159
    Xpos = [] # List of X coordinates on the circle approximation
    Ypos = [] # List of Y coordinates on the circle approximation
    for point in range(n+1):
        X = r * math.sin(2 * pi * point / n)
        Y = r * math.cos(2 * pi * point / n)
        Xpos.append(X)
        Ypos.append(Y)
    for point in range(n+1):
        print("Coors: {} {}".format(Xpos[point], Ypos[point]), file = f)
        
def Center(device, f):
    print("Centering", file=f)
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
    v931.SVO('1',1)
    v931.SVO('2',1)
    v931.RON('1',1)
    v931.RON('2',1)
    print("Axis 1 Referencing", file=f)
    v931.FRF(1)
    time.sleep(15)
    print("Axis 1 Referencing complete", file=f)
    print("Axis 2 Referencing", file=f)
    v931.FRF(2)
    time.sleep(15)
    print("Axis 2 Referencing complete", file=f)
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

def MakeWaves(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_SIN_P(1,int(0.5*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #cos wave
    device.WAV_SIN_P(2,int(0.75*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #sin wave
    device.WAV_SIN_P(3,int(0*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #-cos wave
    device.WAV_SIN_P(4,int(0.25*iNumberOfPoints),iNumberOfPoints,'X',iCenterPointOfWave, 60, -30,iNumberOfPoints) #-sin wave
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)
    
def MakeTriangle(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    #iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_LIN(5,1,iNumberOfPoints,'X', 10, -45, 30,iNumberOfPoints) #y-axis 30 -> -15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 0, -15,iNumberOfPoints) #y-axis -15 -> -15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 45, -15,iNumberOfPoints) #y-axis -15 -> 30 
    device.WAV_LIN(6,1,iNumberOfPoints,'X', 10, 26, 0,iNumberOfPoints) #x-axis 0 -> 26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -52, 26,iNumberOfPoints) #x-axis 26 -> -26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 26, -26,iNumberOfPoints) #x-axis -26 -> 0
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)

def MakeDiamond(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    #iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_LIN(5,1,iNumberOfPoints,'X', 10, -30, 30,iNumberOfPoints) #y-axis 30 -> 0
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -30, 0,iNumberOfPoints) #y-axis 0 -> -30
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 30, -30,iNumberOfPoints) #y-axis -30 -> 0
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 30, 0,iNumberOfPoints) #y-axis 0 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'X', 10, 30, 0,iNumberOfPoints) #x-axis 0 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -30, 30,iNumberOfPoints) #x-axis 30 -> 0
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -30, 0,iNumberOfPoints) #x-axis 0 -> -30
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 30, -30,iNumberOfPoints) #x-axis -30 -> 0
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)

def MakePentagon(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    #iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_LIN(5,1,iNumberOfPoints,'X', 10, -20.73, 30,iNumberOfPoints) #y-axis 30 -> 9.27
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -33.54, 9.27,iNumberOfPoints) #y-axis 9.27 -> -24.27
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 0, -24.27,iNumberOfPoints) #y-axis -24.27 -> -24.27
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 33.54, -24.27,iNumberOfPoints) #y-axis -24.27 -> 9.27
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 20.73, 9.27,iNumberOfPoints) #y-axis 9.27 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'X', 10, 28.53, 0,iNumberOfPoints) #x-axis 0 -> 28.53
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -10.90, 28.53,iNumberOfPoints) #x-axis 28.53 -> 17.63
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -35.26, 17.63,iNumberOfPoints) #x-axis 17.63 -> -17.63
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -10.90, -17.63,iNumberOfPoints) #x-axis -17.63 -> -28.53
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 28.53, -28.53,iNumberOfPoints) #x-axis -28.53 -> 0
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)
    
def MakeHexagon(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    #iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_LIN(5,1,iNumberOfPoints,'X', 10, -15, 30,iNumberOfPoints) #y-axis 30 -> 15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -30, 15,iNumberOfPoints) #y-axis 15 -> -15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -15, -15,iNumberOfPoints) #y-axis -15 -> -30
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 15, -30,iNumberOfPoints) #y-axis -30 -> -15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 30, -15,iNumberOfPoints) #y-axis -15 -> 15
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 15, 15,iNumberOfPoints) #y-axis 15 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'X', 10, 26, 0,iNumberOfPoints) #x-axis 0 -> 26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 0, 26,iNumberOfPoints) #x-axis 26 -> 26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -26, 26,iNumberOfPoints) #x-axis 26 -> 0
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -26, 0,iNumberOfPoints) #x-axis 0 -> -26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 0, -26,iNumberOfPoints) #x-axis -26 -> -26
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 26, -26,iNumberOfPoints) #x-axis -26 -> 0
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)
    
def MakeOctagon(device):
    wgConfigifrequencyOfWave = 30      # frequency of wave
    PARAM_ServoUpdateTime = 234881536
    servoCycleTime = device.qSPA('1',PARAM_ServoUpdateTime)
    #calculate number of point in wavetable from given frequency
    iNumberOfPoints = int((1/(servoCycleTime['1'][234881536] * wgConfigifrequencyOfWave)))
     # curve center point is the middle of the segment
    #iCenterPointOfWave = int(iNumberOfPoints / 2)
#     device.WAV_SIN_P(iWaveTableID,OffsetOfFirstPointInWaveTable,iNumberOfPoints,iAddAppendWave,iCenterPointOfWave, dAmplitudeOfWave, wgConfigdOffsetOfWave,iSegmentLen
    device.WAV_LIN(5,1,iNumberOfPoints,'X', 10, -8.79, 30,iNumberOfPoints) #y-axis 30 -> 21.21
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -21.21, 21.21,iNumberOfPoints) #y-axis 21.21 -> 0
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -21.21, 0,iNumberOfPoints) #y-axis 0 -> -21.21
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, -8.79, -21.21,iNumberOfPoints) #y-axis -21.21 -> -30
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 8.79, -30,iNumberOfPoints) #y-axis -30 -> -21.21
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 21.21, -21.21,iNumberOfPoints) #y-axis -21.21 -> 0
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 21.21, 0,iNumberOfPoints) #y-axis 0 -> 21.21
    device.WAV_LIN(5,1,iNumberOfPoints,'&', 10, 8.79, 21.21,iNumberOfPoints) #y-axis 21.21 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'X', 10, 21.21, 0,iNumberOfPoints) #x-axis 0 -> 21.21
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 8.79, 21.21,iNumberOfPoints) #x-axis 21.21 -> 30
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -8.79, 30,iNumberOfPoints) #x-axis 30 -> 21.21
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -21.21, 21.21,iNumberOfPoints) #x-axis 21.21 -> 0
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -21.21, 0,iNumberOfPoints) #x-axis 0 -> -21.21
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, -8.79, -21.21,iNumberOfPoints) #x-axis -21.21 -> -30
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 8.79, -30,iNumberOfPoints) #x-axis -30 -> -21.21
    device.WAV_LIN(6,1,iNumberOfPoints,'&', 10, 21.21, -21.21,iNumberOfPoints) #x-axis -21.21 -> 0
    device.WTR(1,1,0)
    device.WTR(2,1,0)
    device.WGC(1,0)
    device.WGC(2,0)
    
def DriveWave(device, axis, tableid, f):
    # start wave generator output, data recorder starts simultaneously
    print('Start wavegenerator',file=f)
    device.WSL(axis, tableid)
    #print(device.qGWD())
    if len(axis) == 1:
        device.WGO(axis, 1)
    else: device.WGO(axis, [1,1])
    time.sleep(15)
    print('done', file=f)
    if len(axis) == 1:
        device.WGO(axis, 0)
    else: device.WGO(axis, [0,0])
    
def Driver():
    f = open('logfile.txt', 'w')
    print("triangle", file = f)
    Polygon(3, 30, f)
    print("square", file = f)
    Polygon(4, 30, f)
    print("pentagon", file = f)
    Polygon(5, 30, f)
    print("hexagon", file = f)
    Polygon(6, 30, f)
    print("Octagon", file = f)
    Polygon(8, 30, f)
    f.flush()
    #exit(1)
    time.sleep(10)
    device = StartController(f)
    travelmax1, travelmin1, travelmax2, travelmin2 = GetTravel(device,f)
    axis1 = '1'
    axis2 = '2'
    cos = 1
    sin = 2
    ncos = 3
    nsin = 4
    polygony = 5
    polygonx = 6
    device.VEL(axis1, (5000))
    device.VEL(axis2, (5000))
    f.close()
    while True:
        f = open('logfile.txt', 'a')
        start = time.time()
        
        MakeWaves(device)
        Center(device,f)
        DriveWave(device, axis1, sin, f) #vertical line
        Center(device,f)
        DriveWave(device, axis2, sin, f) #horizontal line
        Center(device,f)
        DriveWave(device, [int(axis1), int(axis2)], [sin, sin],f) #postive line
        Center(device,f)
        DriveWave(device, [int(axis1), int(axis2)], [sin, nsin],f) #negative line
        
        MakeTriangle(device)
        device.MOV([axis1, axis2],[30, 0])
        WaitForMotionDone(device, axis1)
        WaitForMotionDone(device, axis2)
        DriveWave(device, [int(axis1), int(axis2)], [polygony, polygonx],f) #triangle

        MakeDiamond(device)
        device.MOV([axis1, axis2],[-30, -30])
        WaitForMotionDone(device, axis1)
        WaitForMotionDone(device, axis2)
        DriveWave(device, [int(axis1), int(axis2)], [polygony, polygonx],f) #square

        MakePentagon(device)
        device.MOV([axis1, axis2],[30, 0])
        WaitForMotionDone(device, axis1)
        WaitForMotionDone(device, axis2)
        DriveWave(device, [int(axis1), int(axis2)], [polygony, polygonx],f) #pentagon
        
        MakeHexagon(device)
        device.MOV([axis1, axis2],[30, 0])
        WaitForMotionDone(device, axis1)
        WaitForMotionDone(device, axis2)
        DriveWave(device, [int(axis1), int(axis2)], [polygony, polygonx],f) #hexagon
        
        MakeOctagon(device)
        device.MOV([axis1, axis2],[30, 0])
        WaitForMotionDone(device, axis1)
        WaitForMotionDone(device, axis2)
        DriveWave(device, [int(axis1), int(axis2)], [polygony, polygonx],f) #octagon 
 
        Center(device,f)
        DriveWave(device, [int(axis1), int(axis2)], [cos, sin],f) #circle
        end = time.time()
        print(end-start)
        f.close()

if __name__ == '__main__':
    Driver()
