__author__ = 'asc-mbp'

#@todo
#Finish prearm for GPS
#GS msgs and checking improve
#Altitude control   [STAGED]

#@observe
#General altitude changes
#gs_pc not taken off problems?
#Test too much dist


#@Features
#Terrain following                      30  m
#Cancel later reservations


#@production
#   Fences
#   Gimbal on the ground
#   BIF MIN, MAX ALT
#   Auto Land and RTL performance
#   broken Network psql tests

'''
#Critical:
    @production
    @mode changes are not notified

@todo
BUILD GROUND END                                            Part 2 complete, Part 3 remaining
Failsafe (waiting too long for an instruction)


@observe
ALT relative issues


@tests:
Network intolerance
Test BIF
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
import math

#INITIALIZATIONS
print ":/:MAKING CONNECTION"


consts = Constant()
############################################################################
#@INPUTS HERE
mavid = consts.MAV_ID_SIM
mavDrone = mav.connect('192.168.83.12:14559', wait_ready=True)
############################################################################
cloudconn = CloudConn.CloudConn(mavid)
zipquad = quad.ZipQuad()
lastupdated = datetime.datetime.now()

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
#Features       :Uber like notfications
#Requirement    :ROI circle DONE
#Buildtestcases
#1  Make reservation, make another reservation                                          CHECK
#2  failsafe - fence    internal(ON PX4)
#2.1Disavow - fence external(through GS)
#3  failsafe - overtime                                                                 CHECK
#4  reservation 1, reservation 2, cancel res1 when en route to res 1
#5  reservation 1, reservation 2, cancel res1 when at res1 performing circle
#6  reservation 1, reservation 2  -> create override when at res1                       CHECK
#7  reservation 1, reservation 2 -> create override when en route to res1
#8  Reservation 1 - ensure duration is correct                                          CHECK
#9  POINTING direction on circle                                                        CHECK

def modearmtakeoff():
    global lastupdated
    global mavDrone
    global zipquad
    #cloudconn.takeoffdel()
    print "modearmtakeoff: "+str(datetime.datetime.now()) + " VEHICLE MODE CHANGE TO GUIDED"
    mavDrone.mode = mav.VehicleMode("GUIDED")

    print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting to ARM VEHICLE"
    mavDrone.armed = True

    while not mavDrone.armed:
        print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting to ARM VEHICLE"
        time.sleep(0.3)

    print "modearmtakeoff: "+str(datetime.datetime.now()) + " ARMED"
    print "modearmtakeoff: "+str(datetime.datetime.now()) + " attempting TAKEOFF to "+str(consts.TAKEOFF_ALT)+" meters"


    mavDrone.commands.takeoff(consts.TAKEOFF_ALT)   #quad.takeoffalt
    print mavDrone.mode.name
    reached = False
    zipquad.status = consts.TAKING_OFF
    zipquad.dest = mavDrone.home_location

    cloudconn.addflight()
    cloudconn.updateCloud(mavDrone, zipquad)

    while reached == False:
        print "modearmtakeoff: "+str(datetime.datetime.now()) + " current altitude is "+ str(mavDrone.location.global_frame.alt)
        if mavDrone.location.global_frame.alt >= consts.TAKEOFF_ALT*consts.PRECISION:
            reached = True
        else:
            time.sleep(1)

    zipquad.takeofftime = datetime.datetime.now()
    zipquad.status = consts.ZIP_WAIT_INST

    cloudconn.updateCloud(mavDrone, zipquad)

def failsafe():

    expiration = zipquad.takeofftime + datetime.timedelta(seconds=consts.BTRY_TIME)
    #print str(expiration - datetime.datetime.now())
    if expiration <= datetime.datetime.now():
        return True

    return False


def cloudoverride():
    return False

def onlocchange(self,  attr_name, msg):
    global mavDrone, zipquad, lastupdated
    #@Update cloud or get from cloud
    if datetime.datetime.now() >= (datetime.timedelta(seconds=consts.NETWORK_FRQ) + lastupdated):
        lastupdated = datetime.datetime.now()
        cloudconn.updateCloud(mavDrone, zipquad)
        if zipquad.status != consts.ZIP_OVERRIDE or zipquad.status != consts.ZIP_FS:
            #print zipquad.status
            stat, val = cloudconn.getmissions(zipquad)
            #print stat, val
            if stat == consts.ZIP_OVERRIDE:
                #@PRODUCTION CRITICAL DO NOT OVERRIDE THE TX
                if mavid == consts.MAV_ID_SIM:
                    mavDrone.channels.overrides = {}
                print "onlocchange:: Received an override "+str(zipquad.status)
                mavDrone.mode = mav.VehicleMode("RTL")
                zipquad.status = consts.ZIP_OVERRIDE
                zipquad.resid = consts.ZIP_OVERRIDE
                zipquad.dest  = mavDrone.home_location

            elif stat == consts.FLT_CANCELED:
                #@PRODUCTION CRITICAL DO NOT OVERRIDE THE TX
                if mavid == consts.MAV_ID_SIM:
                    mavDrone.channels.overrides = {}
                mavDrone.mode = mav.VehicleMode("LOITER")
                mavDrone.mode = mav.VehicleMode("GUIDED")
                zipquad.status = consts.ZIP_WAIT_INST
                zipquad.mode   = mavid


            elif stat == consts.SUCCESS:
                #@PRODUCTION CRITICAL DO NOT OVERRIDE THE TX
                if mavid == consts.MAV_ID_SIM:
                    mavDrone.channels.overrides = {}

                mavDrone.mode = mav.VehicleMode("GUIDED")
                print str(val["LocationGlobal"])
                mavDrone.commands.goto(val["LocationGlobal"])
                zipquad.dest = val["LocationGlobal"]
                zipquad.resid = val["res_id"]
                zipquad.alt = val["alt"]
                zipquad.dur = val["dur"]
                zipquad.bear   =    val['bearing']
                zipquad.status = consts.ZIP_EN_ROUTE


    #Either waiting instruction, en route, atwp, override
    if zipquad.status != consts.ZIP_OVERRIDE and failsafe() == True:
        if zipquad.status != consts.ZIP_FS:
            #@PRODUCTION CRITICAL DO NOT OVERRIDE THE TX
            if mavid == consts.MAV_ID_SIM:
                mavDrone.channels.overrides = {}
            print "ENTERED FAILSAFE!"
            zipquad.status = consts.ZIP_FS
            zipquad.resid  = mavid
            mavDrone.mode = mav.VehicleMode("RTL")
            cloudconn.overrideotherres()                #Tell other reservations they've been canceled
            return

    if zipquad.status==consts.ZIP_EN_ROUTE:
        if get_distance_metres(zipquad.dest, mavDrone.location.global_frame) <= consts.CIRCLE_OFS:
            print "REACHED DEST"
            zipquad.status = consts.ZIP_AT_RES
            #@PRODUCTION CRITICAL DO NOT OVERRIDE THE TX
            if mavid == consts.MAV_ID_SIM:
                mavDrone.channels.overrides[consts.THROTTLE_OVR] = consts.THR_CENTER
            if zipquad.bear == consts.REQ_PANORAMA:
                mavDrone.parameters['CIRCLE_RADIUS'] = consts.PANORAMA_MODE
            mavDrone.mode = mav.VehicleMode("CIRCLE")
            zipquad.endres = datetime.datetime.now() + datetime.timedelta(seconds=zipquad.dur)
            print str(zipquad.endres)
            cloudconn.updateCloud(mavDrone,zipquad)
            return

    if zipquad.status == consts.ZIP_AT_RES and datetime.datetime.now() >= zipquad.endres:
        print "fly:: onloc Completed reservation time"
        #@PRODUCTION DO NOT OVERRIDE THE TX
        mavDrone.parameters['CIRCLE_RADIUS'] = consts.REMOVE_PANORAMA
        if mavid == consts.MAV_ID_SIM:
            mavDrone.channels.overrides = {}
        zipquad.resid = mavid
        zipquad.status = consts.ZIP_WAIT_INST
        mavDrone.mode = VehicleMode("GUIDED")
        return
    


def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

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
    mavDrone.add_attribute_listener('location', onlocchange)
    while True:
        j=0


fly()