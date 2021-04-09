import cv2
from djitellopy import tello
from time import sleep
import numpy as np
import keyboard

cap = cv2.VideoCapture(0)

FB_RANGE = [5200, 5800]
pid = [0.4, 0.4, 0]
prev_error = 0
w, h = 360, 240
# proportional, integral, derivative
drone = tello.Tello()


drone.connect()
print(drone.get_battery())

drone.streamon()
sleep(1)
print("sending up")


def find_face(img):
    face_cascade = cv2.CascadeClassifier("resources/face.xml")
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_grey, 1.2, 8)

    face_list_c = []
    face_list_area = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cx = x + w//2
        cy = y + h//2
        area = w*h

        face_list_c.append([cx, cy])
        face_list_area.append(area)

        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    if len(face_list_c) > 0:
        index = face_list_area.index(max(face_list_area))
        return img, [face_list_c[index], face_list_area[index]]

    else:
        return img, [[0, 0], 0]


def track_face(drone, info, w, pid, prev_error):
    area = info[1]
    x, y = info[0]
    fb_speed = 0

    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - prev_error)
    speed = int(np.clip(speed, -100, 100))

    # FB_RANGE = [4900, 5800]

    if FB_RANGE[0] < area < FB_RANGE[1]:
        fb_speed = 0

    # if face is too small, come closer
    elif area < FB_RANGE[0] and area != 0:
        fb_speed = 40

    ## if area of face is larger than than 4800 go away
    elif area > FB_RANGE[1]:
        fb_speed = -40

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb_speed)
    drone.send_rc_control(0, fb_speed, 0, speed)
    return error


while True:

    if keyboard.is_pressed('t'):
        drone.takeoff()
        sleep(1)

    img = drone.get_frame_read().frame
    #_, img = cap.read()
    img = cv2.resize(img, (w, h))
    img, info = find_face(img)
    cv2.imshow("Output", img)
    # prev_error = track_face(drone, info, w, pid, prev_error
    prev_error = track_face(drone, info, w, pid, prev_error)
    #print(info[1], info[0])

    if keyboard.is_pressed('q'):
        break;

    if keyboard.is_pressed('u'):
        drone.send_rc_control(0, 0, 20, 0)
        sleep(1)

print("broke")
drone.land()
sleep(1)
