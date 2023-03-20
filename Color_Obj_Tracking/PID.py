import numpy as np

def Pid(pid, pErr, error):
           
    speed = pid[0] * error + pid[1]*(error-pErr)
    speed = int(np.clip(speed, -100, 100))
    pErr = error
    
    return speed

