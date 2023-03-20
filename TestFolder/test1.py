import cv2
import numpy as np

image = np.zeros((800,800,3),dtype=np.uint8)

Angle = 45
distance = 300

position = [int(distance*np.sin(int(Angle))), int(distance*np.cos(int(Angle)))]

cv2.circle(image,(position[0],position[1]),10,(0,255,0),-1)

cv2.imshow("aaaa",image)
cv2.waitKey(0)
cv2.destroyAllWindows()