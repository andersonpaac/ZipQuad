#This is a callback function on pitch changes. (every time the pitch on the vehicle changes this function is called.
#For all intents and purposes this code runs continuously and through the flight

import numpy as np
import dronekit as mav
import math
from Constants import constize
#This function takes inputs of the vehicle, .hgt SRTM file and returns a dictionary {"change":True or False, "alt":TargetAltitude}

cons = constize.Constant()
def terrainfollower_strm3(vehicle, hgtfile ="N40W089.hgt"):

    srtm_dtype = np.dtype([('data', np.uint16, 3601)])

    lat = vehicle.location.globa_frame.lat
    lon = vehicle.location.global_frame.lon
    alt = vehicle.location.global_frame.alt
    lstart = math.floor(lat)
    lonstart = math.floor(lon)
    latrow = round((lat - lstart)* 3600, 0)
    lonrow = round((lon - lonstart)*3600, 0)
    latrow = 3601 - latrow
    data = np.fromfile(hgtfile, dtype=srtm_dtype)
    return cons.SUCCESS, data[latrow][0][lonrow]





