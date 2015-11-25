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

    def getoverrides(self):
        #If there's an override -> None of this matters
        now = datetime.datetime.now() - datetime.timedelta(seconds=self.cons.MIS_LOOKAHEAD)
        SQL = "SELECT * FROM reservations WHERE mission_time >= %s AND mission_type = %s"
        values = (now, self.cons.MTYPE_OVR)
        try:
            self.cur.execute(SQL,values)
            self.conn.commit()
        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::getMissions ERROR: Unable to read from reservations"
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        data = self.cur.fetchall()
        if len(data) > 0:
            return self.cons.SUCCESS, True

        return self.cons.SUCCESS, False

    def getresreqs(self):
        now = datetime.datetime.now() - datetime.timedelta(seconds=self.cons.MIS_LOOKAHEAD)
        SQL = "SELECT * FROM reservations WHERE mission_time >= %s AND mission_type = %s ORDER BY mission_time ASC LIMIT 1"
        query = (now, self.cons.MTYPE_RES_REQ)
        try:
            self.cur.execute(SQL,query)
            self.conn.commit()
        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::getmissions ERROR: Unable to read from reservations"
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH
        data = self.cur.fetchall()
        if len(data)>0:
            return self.cons.SUCCESS, {"stat":True, "id":data[0][self.cons.IND_MIS_ID], "data":data[0]}
        return self.cons.SUCCESS, {"stat":False}


    def isReqCNCL(self, id):
        SQL = "SELECT * FROM reservations WHERE mission_id = %s  AND mission_type = %s"
        values = (id, self.cons.MTYPE_RES_CNCL)
        try:
                self.cur.execute(SQL,values)
                self.conn.commit()

        except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::getmissions ERROR: Unable to read from reservations"
                print e
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        dat_cncl = self.cur.fetchall()
        #Remove this entry and return
        if len(dat_cncl) > 0:
            return self.cons.SUCCESS, True
        return self.cons.SUCCESS, False


    def denyall(self, id):
        SQL  = "UPDATE reservations SET mission_type = %s where mission_id = %s"
        values = (self.cons.MTYPE_RES_DND, id)
        try:
            self.cur.execute(SQL,values)
            self.conn.commit()

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::getmissions ERROR: Unable to read from reservations"
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        return self.cons.SUCCESS, True

    def ackall(self, id):
        SQL  = "UPDATE reservations SET mission_type = %s where mission_id = %s"
        values = (self.cons.MTYPE_RES_ACK, id)
        try:
            self.cur.execute(SQL,values)
            self.conn.commit()

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::getmissions ERROR: Unable to read from reservations"
            print e
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        return self.cons.SUCCESS, True

    def getlatestchange(self, id):
        SQL = "SELECT * FROM reservations WHERE mission_id = %s  AND mission_type = %s ORDER BY mission_time DESC LIMIT 1"
        values = (id, self.cons.MTYPE_RES_CHG)
        try:
                self.cur.execute(SQL,values)
                self.conn.commit()

        except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::getmissions ERROR: Unable to read from reservations"
                print e
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        dat_chg = self.cur.fetchall()
        if len(dat_chg) > 0:
            val = dat_chg[0]
            lat = float(val[self.cons.IND_WP_LAT])
            lon = float(val[self.cons.IND_WP_LON])
            alt = val[self.cons.IND_WP_ALT]
            dur = val[self.cons.IND_WP_DUR]
            bearing = val[self.cons.IND_WP_BEARING]
            loctoret = mav.LocationGlobal(lat, lon, 0, is_relative=True)
            #Set mission type for all instances of this id to acknowledged
            SQL  = "UPDATE reservations SET mission_type = %s where mission_id = %s"
            values = (self.cons.MTYPE_RES_ACK, id)
            try:
                self.cur.execute(SQL,values)
                self.conn.commit()
                return self.cons.SUCCESS, {"stat":True, "LocationGlobal":loctoret, "alt":alt, "dur":dur, "bearing":bearing, "res_id":id}

            except (pg.ProgrammingError and pg.IntegrityError) as e:
                print "CloudConn::getmissions ERROR: Unable to read from reservations"
                print e
                return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

        return self.cons.SUCCESS, {"stat":False}




    #Call this when you're awaiting instructions
    #Must return locglobal, alt, bearing, resid
    #Scenarios
    #   Awaiting instructions gets override
    #   Awaiting instructions gets a new reservation -> make sure this is the first reservation FIFO
    #                                                   make sure changes have not been made to this reservation
    #                                                   make sure same reservation isn't done twice{change mtype}

    def getmissions(self):
        #Get overrides
        stat, val = self.getoverrides()
        if stat == self.cons.SUCCESS:
            if val == True:
                print "CloudConn:getmissions: Found an override"
                return self.cons.ZIP_OVERRIDE, self.cons.ZIP_OVERRIDE

        #No overrides get reservations
        stat, val = self.getresreqs()
        if stat == self.cons.SUCCESS and val["stat"] == True:
            print "CloudConn:getmissions: Found a reservation request"
            valsreq = val["data"]
            res_id = val["id"]
            lat = float(valsreq[self.cons.IND_WP_LAT])
            lon = float(valsreq[self.cons.IND_WP_LON])
            alt = valsreq[self.cons.IND_WP_ALT]
            dur = valsreq[self.cons.IND_WP_DUR]
            bearing = valsreq[self.cons.IND_WP_BEARING]
            loctoret = mav.LocationGlobal(lat, lon, 0, is_relative=True)
            dicttoret = {"stat":True, "LocationGlobal":loctoret, "alt":alt, "dur":dur, "bearing":bearing, "res_id":res_id}

            #Check if canceled
            stat, val = self.isReqCNCL(res_id)
            if stat == self.cons.SUCCESS and val == True:
                print "CloudConn:getmissions: The reservation was canceled, denying request"
                self.denyall(res_id)
                return self.cons.NO_UPDATE, self.cons.NO_UPDATE

            #Check if changed
            stat, val = self.getlatestchange(res_id)
            if stat == self.cons.SUCCESS and val["stat"]==True:
                print "CloudConn:getmissions: The reservation was changed"
                return self.cons.SUCCESS, val


            #Not canceled, Not changed
            self.ackall(res_id)
            return self.cons.SUCCESS, dicttoret

        return self.cons.NO_UPDATE, self.cons.NO_UPDATE


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
    def createreservation(self, wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing):
        self.cur.execute("SELECT count(*) from reservations;")
        count = int(self.cur.fetchall()[0][0])
        id = count + 1
        self.res_id = id
        try:
            SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            now = datetime.datetime.now()
            values = (self.cons.MTYPE_RES_REQ, now, self.res_id, wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing)
            self.cur.execute(SQL,values)
            self.conn.commit()
            print "CloudConn::createreservation success created reservation"
            return self.cons.SUCCESS, self.res_id

        except (pg.ProgrammingError and pg.IntegrityError) as e:
            print "CloudConn::createreservation ERROR: unable to insert into reservations"
            return self.cons.DB_NOT_REACH, self.cons.DB_NOT_REACH

    #@todo Uninitialized reservation id
    def changereservation(self,  wp_lat, wp_lon, wp_alt, wp_dur, bearing):
        SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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
                SQL = "INSERT INTO reservations  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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