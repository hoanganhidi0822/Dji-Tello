from utils import *

# params
# w,h
width = 360
height = 240

# set pid control values
pid = [0.5, 0.5, 0]
pErr = 0

startCounter = 0 # test for no flight = 1, for flight = 0

dim = (width, height)


# init drone
myDrone = initTello()



# main loop
while True:
    # Take off, fly
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    #get frame from tello
    img = telloGetFrame(myDrone, dim)

    # find face
    img_from_tello, inf = findFace(img)
    
    # track face 
    pErr = trackFace(myDrone, inf, width, pid, pErr)

    
    #print(inf[0][0])

    # display
    cv2.imshow('Image', img)

    #stop the drone on q kay (safety measure)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break







