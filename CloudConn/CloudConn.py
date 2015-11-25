__author__ = 'asc-mbp'
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
import psycopg2 as pg
import datetime
from datetime import datetime
from Constants import constize
import os


'''
    Network
        conn -> connection
        cur  -> cursor

    Flight variables
        mav_id  ->  Simulator or quad
        flt_id  ->  Flight ID




'''

import datetime

import dronekit as mav
import time
import psycopg2 as pg

class CloudConn:

    #Make connection
    def __init__(self, mav_id):
        diction = dict(os.environ)
        pwd = diction["ZIPQUAD_PWD"]
        hostip = diction["ZIPQUAD_IP"]
        self.conn = pg.connect(database="zipquad", user="airside", host=hostip, password=pwd)
        self.cur = self.conn.cursor()
        self.mav_id = mav_id
        self.cons = constize.Constant()
        self.flt_id = self.cons.UNINIT
        self.res_id = self.cons.UNINIT
        self.on_ovr = self.cons.UNINIT



    def locationglobaltostringpg(self, locationglobal):
        return str(locationglobal)[15:]

    #Should send location, status(mission, failsafe, available, RTH), battery, velocity, RESSTART
    def updateCloud(self, mavDrone, zipquad):
        location = self.locationglobaltostringpg(mavDrone.location.global_frame)
        timenow = datetime.datetime.now()
        tname = "flt_"+ str(self.flt_id)
        try:
            SQL = "INSERT INTO "+tname+" VALUES (%s,%s,%s)"
            values = (timenow, location, zipquad.status)
            self.cur.execute(SQL,values)
            self.conn.commit()
            return self.cons.SUCCESS, self.cons.SUCCESS

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::updateCloud ERROR: Unable to INSERT into flt_"+str(self.flt_id)
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

    #Remove message from queue
    #def checkcloud(self):


    def addflight(self):
        print "CloudConn::addflight Received request for flight creation"
        #Create a record in flights
        self.cur.execute("SELECT count(*) from flights;")
        count = int(self.cur.fetchall()[0][0])
        id = count + 1
        self.flt_id = id
        self.cur.execute("INSERT INTO flights VALUES(%s,%s,%s,%s,%s)",(self.mav_id, id, datetime.datetime.now(), self.cons.time_UNINIT, self.cons.UNINIT))
        self.conn.commit()
        #Create a table for this flight
        try:
            SQL = "CREATE TABLE flt_" + str(id) +" (mav_time timestamp, location varchar(200), status integer)"
            self.cur.execute(SQL)
            self.conn.commit()
            print "CloudConn::addflight Success Created Table for flight"
            return self.cons.SUCCESS, self.cons.SUCCESS

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::addflight ERROR: Unable to create table "
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

    #wp_dur is in seconds
    #wp_alt is relative
    #wp_lat,wp_lon is string
    def createreservation(self, wp_lat, wp_lon, wp_alt, wp_dur, bearing):
        self.cur.execute("SELECT count(*) from reservations;")
        count = int(self.cur.fetchall()[0][0])
        id = count + 1
        self.res_id = id
        self.cur.execute()
        try:
            SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s)"
            now = datetime.datetime.now()
            values = (self.cons.MTYPE_RES_REQ, now, self.res_id, wp_lat, wp_lon, wp_alt, wp_dur)
            self.cur.execute(SQL,values)
            self.conn.commit()
            print "CloudConn::createreservation success created reservation"
            return self.cons.SUCCESS, self.res_id

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::createreservation ERROR: unable to insert into reservations"
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

    #@todo Uninitialized reservation id
    def changereservation(self,  wp_lat, wp_lon, wp_alt, wp_dur, bearing):
        SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s)"
        now = datetime.datetime.now()
        values = (self.cons.MTYPE_RES_CHG, now, self.res_id, wp_lat, wp_lon, wp_alt, wp_dur, bearing)
        try:
            self.cur.execute(SQL, values)
            self.conn.commit()
            print "CloudConn:: changereservation success changed reservation"
            return self.cons.SUCCESS, self.res_id

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::changereservation ERROR: unable to change reservations"
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

    def isValid(self, override):
        return True

    #@todo override code
    def createoverride(self, overridecode):
        if self.isValid(overridecode):
            try:
                wp_lat = ""
                bearing = 0.0
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s)"
                now = datetime.datetime.now()
                values = (self.cons.MTYPE_OVR, now, self.cons.ZIP_OVERRIDE, wp_lat, wp_lat, 0 , 0, bearing)
                self.cur.execute(SQL, values)
                self.conn.commit()
                print "CloudConn:: createoverride success created Override"
                return self.cons.SUCCESS, self.cons.SUCCESS

            except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::createoverride ERROR: unable to create override USE THE STICKS MATE"
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH
        else:
            return self.cons.OVR_AUTH_FAIL, self.cons.OVR_AUTH_FAIL


    #@todo Uninitialized reservation id
    #UNUSED
    def changebearing(self,bearing):
        try:
                wp_lat = ""
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s)"
                now = datetime.datetime.now()
                values = (self.cons.MTYPE_RES_YAW, now, self.res_id, wp_lat, wp_lat, 0 , 0, bearing)
                self.cur.execute(SQL, values)
                self.conn.commit()
                print "CloudConn:: changebearing success created Override"
                return self.cons.SUCCESS, self.res_id

        except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::changebearing ERROR: unable to change the bearing"
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH


    #@todo Uninitialized reservation id
    def cancelreservation(self,res_id=-1):
        cnclafter = False
        if res_id == -1:
            res_id = self.res_id        #Cancel current reservation
            cnclafter = True
        try:
                wp_lat = ""
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s)"
                now = datetime.datetime.now()
                bearing = 0.0
                values = (self.cons.MTYPE_RES_CNCL, now, res_id, wp_lat, wp_lat, 0 , 0, bearing)
                self.cur.execute(SQL, values)
                self.conn.commit()
                print "CloudConn:: cancelreservation success canceled reservation"
                if cnclafter:
                    res_id = self.cons.UNINIT
                return self.cons.SUCCESS, self.cons.SUCCESS

        except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::CreateRes ERROR: unable to cancel reservation"
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH