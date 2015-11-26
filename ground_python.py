from Constants import constize
from GSBackend import backend
from CloudConn import CloudConn
import datetime
import dronekit as dk
import math
gs = backend.RQClass()
consts = constize.Constant()
cloudconn = CloudConn.CloudConn(consts.GRD_PY)

def welcome():
    print "Welcome to the ECE445 Ground Station for ZipQuad"

def getdata():
    wp_lat_lon = raw_input("Input latitude and longitude of reservation(, delimited):\n")
    wp_lat = wp_lat_lon.split(",")[0].lstrip().rstrip()
    wp_lon = wp_lat_lon.split(",")[1].lstrip().rstrip()
    wp_alt = raw_input("What is the prefered altitude\n")
    try:
        wp_alt = int(wp_alt)
        if wp_alt > 90:
            print "Your altitude request is higher than allowed as mandated by the FAA, defauting to "+str(consts.RES_DEF_TIME)
            wp_alt = consts.RES_DEF_ALT
        elif wp_alt < consts.MIN_ALT:
            print "Your altitude target is too low for that area. Defaulting to " + str(consts.RES_DEF_ALT)
            wp_alt = consts.RES_DEF_ALT
    except ValueError:
        print "Your altitude input is invalid defaulting to "+str(consts.RES_DEF_ALT)
        wp_alt = consts.RES_DEF_ALT
    wp_dur = raw_input("How long would you like your flight?\n")
    try:
        wp_dur = int(wp_dur)
        if wp_dur < consts.RES_MIN_DUR or wp_dur > consts.RES_MAX_DUR:
            print "Your duration input is too high or too low, defaulting to "+str(consts.RES_DEF_TIME)
        wp_dur = consts.RES_DEF_TIME
    except ValueError:
        print "Your duration input is invalid, defaulting to "+str(consts.RES_DEF_TIME)
        wp_dur = consts.RES_DEF_TIME

    stat, val =cloudconn.gettakeofflocation()
    if stat == consts.SUCCESS:
        target = dk.LocationGlobal(float(wp_lat), float(wp_lon), 0, is_relative=False)
        dist = get_distance_metres(target, val)
        if dist < consts.MAX_DIST:
            return consts.SUCCESS, [wp_lat, wp_lon, wp_alt, wp_dur, 0]
        else:
            return consts.TOOFAR, [wp_lat, wp_lon, wp_alt, wp_dur, 0]

    return consts.NO_HOME, [wp_lat, wp_lon, wp_alt, wp_dur, 0]

def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def options():
    if gs.isRes():
        print "You've a reservation with id "+str(gs.res_id)
        print "0. Cancel your reservation"
        print "1. Change your reservation"
        print "2. Change your altitude"
        print "999. Exit"
        opt = raw_input("Enter your option:\n")
        try:
            option = int(opt)
        except ValueError:
            option = -1
            print "You've entered an invalid option."
            return 0
        if option == 0:
            stat, val = gs.cancelReservation()
            if stat==consts.SUCCESS:
                print "You've canceled your reservation"

        elif option == 1:
            stat, vals = getdata()
            if stat == consts.SUCCESS:
                stat1, val1 = gs.changeReservation(vals[0], vals[1], vals[2], vals[3], vals[4])
                if stat1 == consts.SUCCESS:
                    print "Your reservation has been changed"

            elif stat == consts.NO_HOME:
                print "The craft has not been dispatched yet, please wait for the quad to dispatch"
                return
            elif stat == consts.TOOFAR:
                print "Sorry, the waypoint is not in the service radius"
                return


        elif option == 2:
            wp_alt = raw_input("What is your new altitude\n")
            try:
                wp_alt = int(wp_alt)
                stat, val = gs.changeAltitude(wp_alt)
                if stat == consts.SUCCESS:
                    print "Your bearing request has been made"
                else:
                    print "Your bearing request failed to be made"
            except ValueError:
                print "Your bearing input is invalid, cancelling to "+str(consts.RES_DEF_BEAR)

        elif option == 445:
            override = raw_input("Enter access code for OVERRIDE\n")
            stat,val = gs.override(override)
            if stat==consts.SUCCESS:
                print "Your OVERRIDE code is accepted"
            elif stat==consts.OVR_AUTH_FAIL:
                print "Authentication failure"
            elif stat==consts.DB_NOT_REACH:
                print "Auth Succesful but unable to realize DBConn"

        elif option == 999:
            return -1


    else:
        print "You don't have any reservations yet"
        inpt = raw_input("Would you like to create a reservation(y/n)?\n")
        if inpt=="y":
            inpt1 = raw_input("Is this for now or later?")
            if inpt1 == "now" or inpt1 == "n":
                stat, val = getdata()
                if stat == consts.SUCCESS:
                    stat1, val1 = gs.createreservation(val[0], val[1], val[2], val[3], val[4])
                    if stat1 == consts.SUCCESS:
                        print "Your reservation has been created"
                    else:
                        print "DB is not reachable at this time"

                elif stat == consts.NO_HOME:
                    print "The craft has not been dispatched yet, please wait for the quad to dispatch"
                    return

                elif stat == consts.TOOFAR:
                    print "Sorry, the waypoint is not in the service radius"
                    return
            else:
                inpt2 = raw_input("Enter the day and time for the reservation? (12-21-15 04:21 PM)\n")
                try:
                    dat = datetime.datetime.strptime(inpt2, "%m-%d-%y %I:%M %p")
                    if dat < datetime.datetime.now():
                        print "This time is in the past."
                        return
                except ValueError:
                    print "You've not entered it in the right format/ that was not a valid date"
                    return
                stat , val = getdata()
                print "Val returned is "+ str(val)
                if stat == consts.SUCCESS or stat == consts.NO_HOME or consts.TOOFAR:   #@production
                    dict1 = {}
                    dict1["lat"]        =   val[0]
                    dict1["lon"]        =   val[1]
                    dict1["alt"]        =   val[2]
                    dict1["dur"]        =   val[3]
                    dict1["bearing"]    =   val[4]
                    dict1["synctime"]   =   inpt2
                    if stat == consts.NO_HOME or consts.TOOFAR:
                        print "There is no craft that is currently airborne\nYour location might be outside our service(Service not guaranteed)"
                    fd = open(consts.LOG_FILE, "a")
                    fd.write(str(dict1)+"\n")
                    fd.close()
                    exit(0)





        elif inpt == "445":
            override = raw_input("Enter access code for OVERRIDE\n")
            stat,val = gs.override(override)
            if stat==consts.SUCCESS:
                print "Your OVERRIDE code is accepted"
            elif stat==consts.OVR_AUTH_FAIL:
                print "Authentication failure"
            elif stat==consts.DB_NOT_REACH:
                print "Auth Succesful but unable to realize DBConn"

        else:
            return -1
    return 0


def main():
    ext = True
    welcome()
    while ext == True:
        retval = options()
        if retval <0:
            ext = False

main()
