from djitellopy import Tello
import cv2
import matplotlib.pyplot as plt
import numpy as np

width = 360
height = 240

dim = (width, height)


# SET YOUR cv2 data PATH
cascPath = "/home/px/Desktop/repos/tello/DroneFaceTracking/froneFaceTracking/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


# connect to drone
# set starting params
def initTello():
    myDrone = Tello()
    myDrone.connect()

    #set velicties to 0
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0

    # get battery status
    print(myDrone.get_battery())

    # turn off stream
    myDrone.streamoff()

    # stream on
    myDrone.streamon()
    return myDrone

    #get image; (drone, image dimentions)



### get frame from camera
def telloGetFrame(myDrone, dim ):
    frame = myDrone.get_frame_read()
    frame = frame.frame
    frame_r = cv2.resize(frame, (width, height))

    # resize using cv2
    img = frame_r
    return img


def findFace(img):
    # detect

    passed_image = img

    imgGray = cv2.cvtColor(passed_image, cv2.COLOR_BGR2GRAY)


    faces = faceCascade.detectMultiScale(
        imgGray,
        scaleFactor=1.1,
        minNeighbors=5,
        flags=cv2.CASCADE_SCALE_IMAGE
    )


    # track closest face
    centerFace = []
    areaFace = []


    #find all faces and draw rectangle (image, position 1, position 2, colour, thickness)
    for (x, y, w, h) in faces:
        cv2.rectangle(passed_image, (x, y), (x + w, y + h), (255, 255, 255), 3)
        # center x
        cx = x + w//2
        # center y
        cy = y + h//2

        area = w * h

        areaFace.append(area)
        centerFace.append([cx, cy])

    # check if faces are present
    if len(areaFace) !=0:
        # finding index of largest area
        i = areaFace.index(max(areaFace))
        # only return face we want to track
        return img, [centerFace[i], areaFace[i]]
    else:
        return img, [[0, 0], 0]



def trackFace(myDrone, inf, width, pid, pErr):
    
    ## PID control
    # difference between actual info value and  where the position should be (face)
    error = inf[0][0] - width//2
    #kp - proportional gain - speed = kp *error + kd*(error-pErr) - from PID
    speed = pid[0] *error + pid[1]*(error-pErr)
    #clip method
    speed = int(np.clip(speed, -100, 100))

    # print values
    print(speed)



    # check for face
    if inf[0][0] !=0:
        myDrone.yaw_velocity = speed
    else:
        #set velicties to 0
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        myDrone.speed = 0
        error = 0
    
    # send values to drone
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error
