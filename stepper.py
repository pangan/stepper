import sys
import time
import RPi.GPIO as GPIO
import tty, termios
import threading



def getchar():
  #Returns a single character from standard input
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  
  global read_key
  read_key = ch
    
  if ch !='x':
    #print ord(ch)
    threading.Thread(target = getchar).start()




# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
#if sys.argv[2]=='l':
StepPins = [4,17,27,22]
#else:
#StepPins = [18,23,24,25]

# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet

Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]
       
]
"""
Seq = [[1,0,0,0],
       [1,0,0,1],
       [0,0,0,1],
       [0,0,1,1],
       [0,0,1,0],
       [0,1,1,0],
       [0,1,0,0],
       [1,1,0,0]
       
]
"""

StepCount = len(Seq)-1
#if sys.argv[3]=='b':
#	StepDir = -1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise
#else:
StepDir = 1

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 1/float(1000)

# Initialise variables
StepCounter = 0




# Start main loop
global read_key
read_key = ''

threading.Thread(target = getchar).start()
print "Press x to exit!"
while True:
  
  if read_key == 'x':
      GPIO.cleanup()
      exit(1)
  elif read_key == chr(65):
    ''' UP '''
    StepDir = 1
  elif read_key == chr(66):
    ''' Down '''
    StepDir = -1



  for pin in range(0, 4):
    xpin = StepPins[pin]
    #print StepCounter
    #print pin
    if Seq[StepCounter][pin]!=0:
      #print " Step %i Enable %i" %(StepCounter,xpin)
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)

  StepCounter += StepDir

  # If we reach the end of the sequence
  # start again
  if (StepCounter>=StepCount):
    StepCounter = 0
  if (StepCounter<0):
    StepCounter = StepCount

  # Wait before moving on
  time.sleep(WaitTime)
