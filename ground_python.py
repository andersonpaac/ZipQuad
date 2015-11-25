from Constants import constize
from GSBackend import backend

gs = backend.RQClass()
consts = constize.Constant()

def welcome():
    print "Welcome to the ECE445 Ground Station for ZipQuad"

def getdata():
    wp_lat = raw_input("Input latitude of reservation:\n")
    wp_lon = raw_input("Input longitude of reservation:\n")
    wp_alt = raw_input("What is the prefered altitude\n")
    try:
        wp_alt = int(wp_alt)
    except ValueError:
        print "Your altitude input is invalid defaulting to "+str(consts.RES_DEF_ALT)
        wp_alt = consts.RES_DEF_ALT
    wp_bearing = raw_input("What is your bearing\n")
    try:
        wp_bearing = int(wp_bearing)
    except ValueError:
        print "Your bearing input is invalid, defaulting to "+str(consts.RES_DEF_BEAR)
        wp_bearing = consts.RES_DEF_BEAR
    wp_dur = raw_input("How long would you like your flight?")
    try:
        wp_dur = int(wp_dur)
        if wp_dur < 10 or wp_dur > 120:
            print "Your duration input is too high or too low, defaulting to "+str(consts.RES_DEF_TIME)
        wp_dur = consts.RES_DEF_TIME
    except ValueError:
        print "Your duration input is invalid, defaulting to "+str(consts.RES_DEF_TIME)
        wp_dur = consts.RES_DEF_TIME

    return consts.SUCCESS, [wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing]

def options():
    if gs.isRes():
        print "You've a reservation with id "+str(gs.res_id)
        print "0. Cancel your reservation"
        print "1. Change your reservation"
        print "2. Change your bearing"
        print "3. Change your altitude"
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

        elif option == 2:
            wp_bearing = raw_input("What is your new bearing\n")
            try:
                wp_bearing = int(wp_bearing)
                stat, val = gs.changeBearing(wp_bearing)
                if stat == consts.SUCCESS:
                    print "Your bearing request has been made"
                else:
                    print "Your bearing request failed to be made"
            except ValueError:
                print "Your bearing input is invalid, cancelling to "+str(consts.RES_DEF_BEAR)


        elif option == 3:
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
            stat, val = getdata()
            if stat == consts.SUCCESS:
                stat1, val1 = gs.createreservation(val[0], val[1], val[2], val[3], val[4])
                if stat1 == consts.SUCCESS:
                    print "Your reservation has been created"
                else:
                    print "DB is not reachable at this time"
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
#41.283432, -73.077111