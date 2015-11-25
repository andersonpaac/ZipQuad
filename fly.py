__author__ = 'asc-mbp'


'''
    conn = CloudConn()
    conn.getmsg()
    conn.updatecld()


    1- Takeoff
    2- Loiter
    3- quad.status = available
       updatecloud(Force)
       quad.endres = None
       quad.mis_id = -1
       quad.res_dur = -1

    4- Set callback for loc location
            disable callback
            checks()
            updatecloud()
            msg = checkcloud()
            command(msg)
            enable callback

    Initially quad is available
    Quad gets new reservation
    checks()
        #Check if mission should be aborted based on duration
        #Check if failsafes are to be triggered
        if quad.endres != None:
            if quad.endres - curtime < 2:   Less than 2 seconds
                quad.status = available
                quad.endres = None
                quad.completed.append(quad.mis_id)
                quad.mis_id = -1
                quad.res_dur  =
                updatecloud(force->RESEND)

        if (!isvalid(msg.wp)):
            quad.status = failsafe
            quad.endres = None
            if quad.mis_id != -1:
                quad.completed.append(quad.mis_id)
            gotowp(quad.home)
            updatecloud(force)

        #Endres has not been set, set endres as soon as you arrive
        if quad.status == mission and quad.endres == None:
            if dis(quad.curloc, quad.dest) < 5: #Within 5 meters
                updatecloud("RESSTART")
                quad.endres = currtime + quad.res_dur




    command(msg)
        if (msg.mis_id != quad.mis_id and quad.status == available and msg.mission_type == "RES") or (msg.mission_type == "RES_CHG: and quad.status== mission and quad.mis_id == res.mis_id)
            deletecloudmessage()
            quad.status =  mission
            updcloud(force)  #Mission data
            if isvalid(msg.wp):
                quad.dest = msg.wp
                gotowp(msg.wp)
                if msg.mis_id != quad.mis_id:
                    msg.mis_id = quad.mis_id
                    quad.res_dur = validdur(msg.res_dur)


        elif msg.mission_type == "RES_CHG: and msg.mis_id in quad.completed :Changes to an completed/ canceled reservation is illegal
            deletecloudmessage()



        elif msg.mis_id == quad.mis_id and quad.status == mission and msg.mission_type == "RES":
            pushtotail(msg)

        elif msg.res_id == quad.res_id  and quad.status == mission and msg.mission_type == "RES_CHG" :
            if quad.dest == msg.wp:     #quad's destination is where we're going



MISSION TYPE    MISSION ID  WP_DATA    DURATION
    RES             12       WP         3
    OVERRIDE        -1       WP
    RES_CNCL
    RES_CHG                             0

QUAD:
    Override
    Failsafe
    RES
    available




'''


import dronekit as mav
import datetime
from Constants.constize import Constant
from dronekit import *
from dronekit import connect
from dronekit.lib import VehicleMode, LocationGlobal
from pymavlink import mavutil
import time
from CloudConn import  CloudConn
from Quad import quad

#INITIALIZATIONS
print ":/:MAKING CONNECTION"


consts = Constant()
############################################################################
#@INPUTS HERE
mavid = consts.MAV_ID_SIM
mavDrone = mav.connect('192.168.1.5:14555', wait_ready=True)
############################################################################
cloudconn = CloudConn.CloudConn(mavid)
zipquad = quad.ZipQuad()


def check(PREARM_MSG):
    return True


#Pre arm checks on vehicle have been removed from AP.
#All checks happen through software.
def prearmChecks():
    global mavDrone

    #ALL CHECKS
    checks = [consts.ARM_GPS, consts.ARM_SATS, consts.ARM_BATS, consts.ARM_CLD]

    while mavDrone.mode.name == "INITIALISING":
        print "arm-checks: "+str(datetime.datetime.now())+ " waiting to complete INIT"
        time.sleep(1)

    stat = True
    for each in checks:
        stat = stat and check(each)
        print "arm-checks: "+str(datetime.datetime.now()) + str(each) + " check returned "+ str(stat)

    print "arm-checks: "+str(datetime.datetime.now()) + " is returning "+str(stat)
    return stat

def modearmtakeoff():
    global mavDrone
    print "modearmtakeoff: "+str(datetime.datetime.now()) + " VEHICLE MODE CHANGE TO GUIDED"
    mavDrone.mode = mav.VehicleMode("GUIDED")

    print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting to ARM VEHICLE"
    mavDrone.armed = True

    while not mavDrone.armed:
        print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting to ARM VEHICLE"
        time.sleep(0.3)

    print "modearmtakeoff: "+str(datetime.datetime.now()) + " ARMED"
    print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting TAKEOFF to"+str(consts.TAKEOFF_ALT)


    mavDrone.commands.takeoff(consts.TAKEOFF_ALT)   #quad.takeoffalt
    print mavDrone.mode.name
    reached = False
    zipquad.status = consts.TAKING_OFF
    zipquad.dest = consts.TAKING_OFF

    cloudconn.addflight()
    cloudconn.updateCloud(mavDrone, zipquad)
    while reached == False:
        print "modearmtakeoff: "+str(datetime.datetime.now()) + " current altitude is "+ str(mavDrone.location.global_frame.alt)
        if mavDrone.location.global_frame.alt >= consts.TAKEOFF_ALT*consts.PRECISION:
            reached = True
        else:
            time.sleep(1)

    cloudconn.updateCloud(mavDrone, zipquad)
    print "modearmtakeoff: "+str(datetime.datetime.now()) + " setting quad to LOITER"


    return consts.SUCCESS, consts.SUCCESS



'''
This is the main function
'''
def fly():
    global mavDrone
    #Run Prearmchecks
    mavDrone.mode = mav.VehicleMode("POSHOLD")
    if mavDrone.armed==True and mavid==consts.MAV_ID_SIM:   #This is  a simulator that was already on
        mavDrone.mode = mav.VehicleMode("RTL")
        print "fly: Simulator running wasn't closed, needs to go home"
        while mavDrone.armed:
            time.sleep(1)
        print "fly: Simulated quad is back home"

    while(prearmChecks() == False):
        print "fly: " + str(datetime.datetime.now()) + " waiting on prearmchecks()"
        time.sleep(1)

    print "fly: " + str(datetime.datetime.now()) + " ARMING MOTORS"
    modearmtakeoff()
    #reservation_destination = LocationGlobal(40.096309, -88.217972, 10, is_relative=True)



fly()