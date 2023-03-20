import cv2
import numpy as np
import math
from djitellopy import tello
import PID
import  Yellow_Obj

pidYaw = [0.35, 0.05, 0]
pidUD =[0.5,0,0]
pid = [0.7,0.6,0]

pErr = 0
pErrY = 0
pErrUD = 0

distanceLim = 30
W = 5.5
f = 440

left_right_velocity=0
forward_backward_velocity=0
up_down_velocity=0
yaw_velocity=0

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()

while True:
    Frame = drone.get_frame_read().frame
    Frame =cv2.resize(Frame,(360,240))
    #hight,width,_ = frame.shape #(480,640)
    Frame, contours = Yellow_Obj.Yellow_Object(Frame)

    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        area =cv2.contourArea(contour)
        toado = ((x+ (x+w))//2,(y+(y+h))//2)
        center = ((Frame.shape[0])//2,(Frame.shape[1]//2))
        
        #print(int(d))
        '''f = (w*21)/W
        print(f)'''
        
        if area > 1000:
            cv2.rectangle(Frame,(x,y),(x+w,y+h),(0,255,0),3)
            
            d = (W*f)/w

            error = d - distanceLim
            error_Yaw = toado[0] - center[1]
            error_UD = toado[1] - center[0]
            
            if toado[0] <= 15 or toado[0] >= 625 or toado[1] <= 15 or toado[1] >= 465:
                error_Yaw = 0
                error = 0
                error_UD = 0
            
            SpeedYaw = PID.Pid(pid = pidYaw, pErr = pErrY, error = error_Yaw)
            Speed = PID.Pid(pid = pid, pErr = pErr, error = error)
            Updown = PID.Pid(pid = pidUD, pErr = pErrUD, error = error_UD)
           
            drone.send_rc_control(left_right_velocity=0, forward_backward_velocity=Speed, up_down_velocity=Updown, yaw_velocity=-SpeedYaw)
            
    #print(pid[0])         
    cv2.imshow("Frame",Frame)
    key = cv2.waitKey(1) & 0xff
    if key ==  ord("q"):
        drone.land()
        break
    elif key == ord('p'):
        pid[0] += 0.05
    elif key == ord('m'):
        pid[0] -= 0.05
    elif key == ord('='):
        pidYaw[0] += 0.05
    elif key == ord('-'):
        pidYaw[0] -= 0.05
#.release()
cv2.destroyAllWindows()