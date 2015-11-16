__author__ = 'asc-mbp'


class Constant:

    def __init__(self):
        #ARM CHECKS
        self.ARM_GPS    =   101     #3D FIX
        self.ARM_SATS   =   102     #Require 6 min sats
        self.ARM_BATS   =   103     #Require battery health high
        self.ARM_CLD    =   104     #Requires the cloud to be reachable at time of arm

        #ZipQuad
        self.ZIP_AVL    =  201      #ZIPQUAD IS available
        self.ZIP_MISS   =  202      #Zipquad is in a mission
        self.ZIP_OVR    =  203      #Zipquad is in an override
        self.ZIP_FS     =  204      #Zipquad is in a failsafe