from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
import time
import math

def Polygon(pidevice, n, r, loopval):
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
        X = r * math.sin(2 * pi * point / n)
        Y = r * math.cos(2 * pi * point / n)
        Xpos.append(X)
        Ypos.append(Y)
    loopcount = 0
    while loopcount < loopval:
        for point in range(n):
            v931.MOV('1', Xpos[point])
            v931.MOV('2', Ypos[point])
            WaitForMotionDone(v931, 1)
            WaitForMotionDone(v931, 2)
        loopcount +=1
        
        
        
def Spiral(pidevice, n, r, loopval):
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
        X = r * point / n * math.sin(2 * pi * point / n)
        Y = r * point / n * math.cos(2 * pi * point / n)
        Xpos.append(X)
        Ypos.append(Y)
    loopcount = 0
    while loopcount < loopval:
        for point in range(n):
            v931.MOV('1', Xpos[point])
            v931.MOV('2', Ypos[point])
            WaitForMotionDone(v931, 1)
            WaitForMotionDone(v931, 2)
        loopcount +=1


def WaitForMotionDone(device, axis):
    isMoving = True
    while isMoving:
        isMoving = device.IsMoving(axis)[axis]





gateway = PISerial("/dev/ttyUSB0", 115200)
messages = GCSMessages(gateway)
v931 = GCSCommands(gcsmessage = messages)

print(v931.qIDN())

v931.SVO('1',1)
print(v931.qSVO('1'))
v931.SVO('2',1)
print(v931.qSVO('2'))


v931.RON('1',1)
print(v931.qRON('1'))
v931.RON('2',1)
print(v931.qRON('2'))

print("Axis 1 Referencing")
v931.FRF(1)
referencing = False
while not referencing:
    referencing = v931.IsControllerReady()
print("Axis 1 Referencing complete")

print("Axis 2 Referencing")
v931.FRF(2)
referencing = False
while not referencing:
    referencing = v931.IsControllerReady()
print("Axis 2 Referencing complete")



# Grabbing Travel Ranges
travelmax1 = v931.qTMX('1')['1'] - 5
travelmin1 = v931.qTMN('1')['1'] + 5
print("{} {}".format(travelmax1, travelmin1))
travelmax2 = v931.qTMX('2')['2'] - 5
travelmin2 = v931.qTMN('2')['2'] + 5
print("{} {}".format(travelmax2, travelmin2))

loopcount = 0


# print("Centering")
# v931.MOV('1', 0)
# v931.MOV('2', 0)
# WaitForMotionDone(v931, 1)
# WaitForMotionDone(v931, 2)
# #time.sleep(5)
# 
# 
# #Vertical lines
# print("Vertical Lines")
# while loopcount < 5:
#     v931.MOV('1', travelmax1)
#     WaitForMotionDone(v931, 1)
#     v931.MOV('1', travelmin1)
#     WaitForMotionDone(v931, 1)
#     loopcount +=1
# loopcount = 0
# v931.MOV('1', 0)
# WaitForMotionDone(v931, 1)
# 
# #Horizontal lines
# print("Horizontal Lines")
# while loopcount < 5:
#     v931.MOV('2', travelmax2)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 2)
#     loopcount +=1
# loopcount = 0
# v931.MOV('2', 0)
# WaitForMotionDone(v931, 2)
# 
# #Positive Diagonal lines
# print("Positive Diagonal Lines")
# while loopcount < 5:
#     v931.MOV('1', travelmax1)
#     v931.MOV('2', travelmax2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('1', travelmin1)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     loopcount +=1
# loopcount = 0
# v931.MOV('1', 0)
# v931.MOV('2', 0)
# WaitForMotionDone(v931, 1)
# WaitForMotionDone(v931, 2)
# 
# #Negative Diagonal lines
# print("Negative Diagonal Lines")
# while loopcount < 5:
#     v931.MOV('1', travelmax1)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('1', travelmin1)
#     v931.MOV('2', travelmax2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     loopcount +=1
# loopcount = 0
# # v931.MOV('1', 0)
# # v931.MOV('2', 0)
# # WaitForMotionDone(v931, 1)
# # WaitForMotionDone(v931, 2)
# 
# #Triangle
# print("Triangle")
# Polygon(v931, 3, 30, 5)
# 
# #Diamond
# print("Diamond")
# Polygon(v931, 4, 30, 5)
# #
# #Square
# print("Square")
# while loopcount < 5:
#     v931.MOV('1', travelmax1)
#     v931.MOV('2', travelmax2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('1', travelmin1)
#     WaitForMotionDone(v931, 1)
#     v931.MOV('2', travelmax2)
#     WaitForMotionDone(v931, 2)
#     v931.MOV('1', travelmax1)
#     WaitForMotionDone(v931, 1)
#     loopcount += 1
# loopcount = 0
# 
# #
# 
# #Pentagon
# print("Pentagon")
# Polygon(v931, 5, 30, 5)
# 
# #Hexagon
# print("Hexagon")
# Polygon(v931, 6, 30, 6)
# 
# #Vertical Linear Raster Scan
# print("Vertical Linear Raster Scan")
# print("Axis 1 Scanning, Axis 2 Stepping")
# while loopcount < 5:
#     v931.VEL('1', 100*(loopcount+1))
#     v931.VEL('2', 100*(loopcount+1))
#     v931.MOV('1', travelmin1)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     for row in range(int(travelmin2), int(travelmax2), 1):
#         if row % 2 == 0:
#             v931.MOV('1', travelmax1)
#             WaitForMotionDone(v931, 1)
#             v931.MOV('2', row + 1)
#             WaitForMotionDone(v931, 2)
#         if row % 2 == 1:
#             v931.MOV('1', travelmin1)
#             WaitForMotionDone(v931, 1)
#             v931.MOV('2', row + 1)
#             WaitForMotionDone(v931, 2)
#     loopcount +=1
# loopcount = 0
# 
# 
# 
# 
# #Horizontal Linear Raster Scan
# print("Horizontal Linear Raster Scan")
# print("Axis 1 Stepping, Axis 2 Scanning")
# while loopcount < 5:
#     v931.VEL('1', 100*(loopcount+1))
#     v931.VEL('2', 100*(loopcount+1))
#     v931.MOV('1', travelmin1)
#     v931.MOV('2', travelmin2)
#     WaitForMotionDone(v931, 1)
#     WaitForMotionDone(v931, 2)
#     for row in range(int(travelmin1), int(travelmax1), 1):
#         if row % 2 == 0:
#             v931.MOV('2', travelmax2)
#             WaitForMotionDone(v931, 2)
#             v931.MOV('1', row + 1)
#             WaitForMotionDone(v931, 1)
#         if row % 2 == 1:
#             v931.MOV('2', travelmin2)
#             WaitForMotionDone(v931, 2)
#             v931.MOV('1', row + 1)
#             WaitForMotionDone(v931, 1)
#         
#     loopcount +=1
# loopcount = 0
# 
# #Constant Velocity Concentric Circle Scan 
# print("Constant Velocity Concentric Circle Scan")
# outerloopcount = 0
# while outerloopcount < 5:
#     v931.VEL('1', 100*(loopcount+1))
#     v931.VEL('2', 100*(loopcount+1))
#     while loopcount < 5:
 #           v931.VEL('1', 100*(loopcount+1))
#            v931.VEL('2', 100*(loopcount+1))
#         Polygon(v931, 20, (loopcount+1)*0.2*travelmax1, 1)
#         loopcount +=1
#     loopcount = 0
#     outerloopcount += 1
# outerloopcount = 0
# 
# #Constant Frequency Concentric Circle Scan 
# print("Constant Frequency Concentric Circle Scan")
# while outerloopcount < 5:
#     while loopcount < 5:
#         distance = (loopcount+1)*0.4*travelmax1*3.14159
#         speed = int(distance / 2)
#         v931.VEL('1', speed)
#         v931.VEL('2', speed)
#         Polygon(v931, 20, (loopcount+1)*0.2*travelmax1, 1)
#         loopcount +=1
#     loopcount = 0
#     outerloopcount +=1
# outerloopcount = 0


#Constant Velocity Spiral Scan 
print("Constant Velocity Spiral Scan")
outerloopcount = 0
while loopcount < 5:
    v931.VEL('1', 100*(loopcount+1))
    v931.VEL('2', 100*(loopcount+1))
    Spiral(v931, 20, (loopcount+1)*0.2*travelmax1, 1)
    loopcount +=1
loopcount = 0

# #Constant Frequency Spiral Scan 
# print("Constant Frequency Spiral Scan")
# while outerloopcount < 5:
#     while loopcount < 5:
#         distance = (loopcount+1)*0.4*travelmax1*3.14159
#         speed = int(distance / 2)
#         v931.VEL('1', speed)
#         v931.VEL('2', speed)
#         Spiral(v931, 20, (loopcount+1)*0.2*travelmax1, 1)
#         loopcount +=1
#     loopcount = 0
#     outerloopcount +=1
# outerloopcount = 0















#while True:
 #   time.sleep(5)
 #   file = pidevice.qPOS()
  #  print(file)

gateway.close()