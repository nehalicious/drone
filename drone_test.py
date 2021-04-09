from djitellopy import tello
from time import sleep
import cv2
import keyboard

drone = tello.Tello()

drone.connect()

print(drone.get_battery())

# drone.streamon()
#
# while True:
#     img = drone.get_frame_read().frame
#     img = cv2.resize(img, (360, 240)  )
#     cv2.imshow("Drone image", img)
#     cv2.waitKey(1)

print("running")

while True:
    try:
        if keyboard.is_pressed('q'):
            drone.takeoff()
            sleep(1)
        if keyboard.is_pressed('f'):
            drone.send_rc_control(0, 20, 0, 0)
            sleep(1)
        if keyboard.is_pressed('u'):
            drone.send_rc_control(0, 0, 20, 0)
            sleep(1)
        if keyboard.is_pressed('l'):
            drone.land()
            sleep(1)
    except:
        drone.land()
