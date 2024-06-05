from pypiano import Piano
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from time import sleep

#  --- CONTROL PARAMETERS ----
videoSource = 1  # index of the video camera source (if more than 1)
winWidth = 1920  # window WIDTH
winHigh = 1080   # window HEIGHT
precision = 0.8  # detection precision

fingerTipsLM = [8, 12, 16, 20]   # these are the landmark points of the tips of each of the 5 fingers
# fingerTipsLM = [8]   # these are the landmark points of the tips of each of the 5 fingers

whiteKeySize = [100, 500]    # width & height of the WHITE KEY
whiteKeyColor = (255, 255, 255)  # default WHITE KEY color
pressedWhiteKeyColor = (160, 77, 236)  # pressed WHITE KEY color, LIGHT PURPLE
blackKeySize = [100, 300]    # width & height of the BLACK KEY
blackKeyColor = (0, 0, 0)  # default BLACK KEY color
pressedBlackKeyColor = (82, 0, 152)  # pressed BLACK KEY color, DARK PURPLE
keyOffset = 40   # the distance between the keys
keyBoardOrigin = [10, 0]
octave = [["C",  "D", 'E', "F",  "G",  "A",  "B"],      # this is the content of one octave
          ["C#", "D#", "", "F#", "G#", "A#", ""]]   # the empty "" is for the E#,B# - they don't exist
numOctaves = 2

instrumentsList = (     # instruments list
    'Acoustic Grand Piano',
    'Bright Acoustic Piano',
    'Electric Grand Piano',
    'Honky-tonk Piano',
    'Electric Piano 1',
    'Electric Piano 2',
    'Harpsichord',
    'Clavi'
)
instrument = 0  # index of the instrument from the list
p = Piano()
p.load_instrument(instrumentsList[instrument])

clickDistance = 65  # the click trigger distance between the fingertip and finger-mcp

vCap = cv2.VideoCapture(videoSource, cv2.CAP_DSHOW)
vCap.set(3, winWidth)
vCap.set(4, winHigh)

detector = HandDetector(detectionCon=precision)

def drawNotes(img, keytype, txt, x, y):
    if keytype == 'w':
        cv2.putText(img, txt, (x, y), cv2.FONT_HERSHEY_PLAIN, 4, blackKeyColor, 3)
    elif keytype == 'b':
        cv2.putText(img, txt, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, whiteKeyColor, 2)
    else:
        pass

def drawAll(img, keylist):
    for kl in keylist:
        x, y = kl.pos
        w, h = kl.size
        kc = kl.color
        kt = kl.keyType
        cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), kc, cv2.FILLED)
        drawNotes(img, kt, kl.text, int(x + w/2 - 15), int(y + h - 10))
    return img

class Key():
    def __init__(self, pos, text, size, color, keyType, octave):
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.keyType = keyType  # 'w' || 'b' - white or black
        self.octave = octave

keyList = []        # list of all keys with their types, coordinates, noteNames, etc.
x0, y0 = keyBoardOrigin
ww, wh = whiteKeySize
bw, bh = blackKeySize
for o in range(numOctaves):
    for i in range(len(octave)):
        for j, k in enumerate(octave[i]):
            wx = o * 7 * (ww + keyOffset) + j * (ww + keyOffset) + x0  # the x coordinate of each WHITE KEY in all octaves
            if i == 0: #white keys
                keyList.append(Key([wx, y0], k, whiteKeySize, whiteKeyColor, 'w', o))
            elif k != "":
                keyList.append(Key([wx + ww - bw / 2 + keyOffset / 2, y0], k, blackKeySize,blackKeyColor, 'b', o))
            else:
                # keyList.append(Key([0, 0], k, [0, 0], blackKeyColor, ''))
                pass

while True:
    success, img = vCap.read()
    flipImg = cv2.flip(img, 1)
    img = detector.findHands(flipImg)
    lmList, bboxInfo = detector.findPosition(flipImg)  # hand landMark points
    flipImg = drawAll(flipImg, keyList)

    if lmList:  # a hand is detected
        for k in keyList:
            x, y = k.pos
            w, h = k.size
            kt = k.keyType
            ko = k.octave
            sep = 0     # vertical detection separator between white and black keys
            if kt == 'w':
                sep = blackKeySize[1]
            for ft in fingerTipsLM:    # check each landmark point of the 5 fingers
                if x < lmList[ft][0] < x + w and (y + sep) < lmList[ft][1] < (y + h):
                    l, _, _ = detector.findDistance(ft, ft - 3, flipImg, draw = False)    #get the distance
                    if l < clickDistance:                                               #check for click (distance bellow given value)
                        cv2.rectangle(flipImg, (int(x), int(y)), (int(x+w), int(y+h)), pressedWhiteKeyColor, cv2.FILLED)    #draw pressed key
                        drawNotes(flipImg, kt, k.text, int(x + w/2 - 15), int(y + h - 10))
                        p.play(k.text + "-" + str(ko + 7//numOctaves))
                        #sleep(0.5)

    cv2.imshow("AI Motion Piano", flipImg)
    k = cv2.waitKey(1)

    if k == 27:     # press <ESC> to exit the app
        break

vCap.release()
cv2.destroyAllWindows()
