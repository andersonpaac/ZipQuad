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
        #self.ZIP_OVR        =   203      #Zipquad is in an override
        #self.ZIP_FS         =   204      #Zipquad is in a failsafe


        #MAV_STATUS
        self.TAKING_OFF     =   3211
        self.LANDING        =   3311
        self.ZIP_EN_ROUTE   =   3411
        self.ZIP_AT_RES     =   3511
        self.ZIP_OVERRIDE   =   3611
        self.ZIP_FS         =   3711
        self.ZIP_WAIT_INST  =   3811



        #MAV_ID
        self.MAV_ID_SIM     =   1000
        self.MAV_ID_ACTUAL  =   445
        self.GRD_PY         =   455
        self.GRD_DAEMON     =   599
        #AIRSIDE TIME


        #GENERIC
        self.UNINIT         =   -200
        self.time_UNINIT    =   datetime.datetime(1993,6,3,23,47,12)
        self.SUCCESS        =   200
        self.DB_NOT_REACH   =   -911
        self.NO_UPDATE      =   350
        self.FLT_CANCELED   =   191


        #RES_PARAMS
        self.FAIL_NOTINRES  =   50
        self.FAIL_CANT_CNCL =   55

        self.RES_DEF_TIME   =   40
        self.RES_DEF_ALT    =   32         #@production    Tailor stitch these for BIF
        self.RES_DEF_BEAR   =   100
        self.OVR_AUTH_FAIL  =   -449
        self.RES_MAX_DUR    =   120                      #@production This is the maximum amount of time a reservation can take
        self.RES_MIN_DUR    =   30

        #AIR_PARAMS
        self.TAKEOFF_ALT    =   20          #@production In meters
        self.PRECISION      =   0.95        #Overshoot control for altitude
        self.WP_DIST        =   2
        self.CRUISE_ALT     =   30          #@PRODUCTION
        self.BTRY_TIME      =   6000        #@production
        self.MAX_DIST       =   1300        #@production    in meters
        self.MAX_ALT        =   90          #@production
        self.MIN_ALT        =   30          #@production

        #REALTIME CONTROL
        self.TIME_LOC_CALLB =   5
        self.time_ARM       =   0.2
        self.time_TKOFF     =   0.2
        self.MIS_LOOKAHEAD  =   600         #Number of seconds before now for valid missions

        #NETWORKING AND THROTTLING
        self.NETWORK_FRQ    =   3           #Frequency of updates


        #GROUND END
        self.MTYPE_RES_REQ  =   6000
        self.MTYPE_RES_CNCL =   6100
        self.MTYPE_RES_CHG  =   6200
        self.MTYPE_RES_YAW  =   6300
        self.MTYPE_RES_DND  =   6400                    #Cloud denied the request to service as it was either canceled or due to out of bounds
        self.MTYPE_RES_ACK  =   6500                    #Cloud has acknowledged the request of this reservation and is en route
        self.MTYPE_OVR      =   6600
        self.MTYPE_FS       =   6700
        self.NO_HOME        =   4200
        self.TOOFAR         =   4500
        self.LOG_FILE       =   "futuresync.quad"
        self.SYNC_INTERVAL  =   10                      #This is the refresh rate for the daemon


        #RESERVATIONS_INDICES
        self.IND_MIS_TYPE   =   0
        self.IND_MIS_TIME   =   1
        self.IND_MIS_ID     =   2
        self.IND_WP_LAT     =   3
        self.IND_WP_LON     =   4
        self.IND_WP_ALT     =   5
        self.IND_WP_DUR     =   6
        self.IND_WP_BEARING =   7


        #SIM ONLY WARN
        self.THROTTLE_OVR   =   '3'
