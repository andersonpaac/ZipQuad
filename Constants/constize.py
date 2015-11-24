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


        #MAV_STATUS
        self.TAKING_OFF     =   3211
        self.LANDING        =   3311
        self.EN_ROUTE_WP    =   3411
        self.AT_RES         =   3511
        self.OVERRIDE       =   3611
        self.AWAITING_INST  =   3711

        #MAV_ID
        self.MAV_ID_SIM     =   1000
        self.MAV_ID_ACTUAL  =   445

        #AIRSIDE TIME


        #GENERIC
        self.UNINIT         =   -200
        self.time_UNINIT    =   datetime.datetime(1993,6,3,23,47,12)
        self.SUCCESS        =   200
        self.DB_NOT_REACH   =   -911


        #Parameters
        self.TAKEOFF_ALT    =   10          #In meters
        self.PRECISION      =   0.95        #Overshoot control