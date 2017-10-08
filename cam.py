#/usr/bin/env python
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import serial
from web_if import*
from clocko import*
from facializer import isCorrectFace

# Basic setup
FACE_FILENAME = 'QuantumDagan.jpg'
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='geo.log',level=log.INFO)

log.info("Starting video capture")
print('Start vid capture')
video_capture = None
while True:
    for cam_id in [0, 1, 2, 3, 4, 5]:
        print('Checking cam_id '+str(cam_id))
        video_capture = cv2.VideoCapture(cam_id)
        if video_capture.isOpened():
            break
        else:
            video_capture = None
    if video_capture != None:
        break
    print("Failed to connect to camera - retrying...")
    time.sleep(2)
anterior = 1
from hw_if import*
frames = 0

cam_width = video_capture.get(3)
cam_height = video_capture.get(4)
cam_height = 288
y_tolerance = 50
x_tolerance = 200

MAX_FRAMES_FOR_MOVEMENT = 2000
MAX_FRAMES_FOR_ROTATION = 1000

low_x = cam_width/2 - x_tolerance
high_x = cam_width/2 + x_tolerance
low_y = cam_height/2 - y_tolerance
high_y = cam_height/2 + y_tolerance

while True:
    if not video_capture.isOpened():
        log.info('Unable to load camera.')
        print('oh no')
        exit()

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)#orig: 30x30
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        center_x = (2*x+w)/2
        center_y = (2*y+h)/2
        width = w
        height = h
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), 2)
        frames = getTime()

        print(len(faces))
        cv2.imwrite(FACE_FILENAME, frame[y:y+h, x:x+w])
        if(isCorrectFace(FACE_FILENAME)):
            print('HOLY DUCKSHITS GUYS ITS DAGAN OUR BEST FRIEND/DADDY')

        if center_x > low_x and center_x < high_x:
            moveForward() 
            print("move_forward")
        elif center_x<=low_x:
            rotateRight()
            print("rot_right")
        else:
            rotateLeft()
            print("rot_left")


        if anterior != len(faces):
                anterior = len(faces)
    if movingForward():
        frames += 1
        if len(faces) == 0:
            if getTime() - frames > MAX_FRAMES_FOR_MOVEMENT:
                stop()
    if rotatingLeft() or rotatingRight():
        frames += 1
        if len(faces) == 0:
            if getTime() - frames > MAX_FRAMES_FOR_ROTATION:
                stop()


    # Display the resulting frame


    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Display the resulting frame

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
