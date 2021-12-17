from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands


gateway = PISerial("/dev/ttyUSB0", 115200)
messages = GCSMessages(gateway)
V524 = GCSCommands(gcsmessage = messages)

print(V524.qIDN())