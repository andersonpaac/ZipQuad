__author__ = 'asc-mbp'

import datetime


class Constant:

    def __init__(self):
        #ARM CHECKS
        self.ARM_GPS        =   101     #3D FIX
        self.ARM_SATS       =   102     #Require 6 min sats
        self.ARM_BATS       =   103     #Require battery health high
        self.ARM_CLD        =   104     #Requires the cloud to be reachable at time of arm

        #ZipQuad
        self.ZIP_AVL        =   201      #ZIPQUAD IS available
        self.ZIP_MISS       =   202      #Zipquad is in a mission
        self.ZIP_OVR        =   203      #Zipquad is in an override
        self.ZIP_FS         =   204      #Zipquad is in a failsafe


        #MAV_ID
        self.MAV_ID_SIM     =   1000
        self.MAV_ID_ACTUAL  =   445

        #AIRSIDE TIME


        #GENERIC
        self.UNINIT         =   -200
        self.time_UNINIT    =   datetime.datetime(1993,6,3,23,47,12)



        #Parameters
        self.TAKEOFF_ALT    =   10          #In meters
        self.PRECISION      =   0.95        #Overshoot control