from CloudConn import CloudConn
from Constants import constize
import datetime
#Requirements - Run this before any takeoff or reservations


consts = constize.Constant()
mav_id = consts.GRD_UBER

def main():
    cloudconn = CloudConn.CloudConn(mav_id)
    ackd = []
    denied = []
    lastupdated = datetime.datetime.now() - datetime.timedelta(seconds=consts.SYNC_UBER_INT)
    while True:
        if datetime.datetime.now() >= lastupdated + datetime.timedelta(seconds=consts.SYNC_UBER_INT):
            stat, val = cloudconn.getacks()
            #Get all the acks, these are the ones that are being serviced
            #Get all the denies, these are the ones that have been denied or canceled
            if stat == consts.SUCCESS:
                for each in val:
                    if each[0] == consts.ZIP_OVERRIDE:
                        print "ZipQuad services are non-operational due to an override."
                        exit(0)
                    if each[0] not in ackd:
                        print "ZipQuad has accepted reservation id "+str(each[0])+" and is en route to you"
                        ackd.append(each[0])

            stat, val = cloudconn.getdenied()
            if stat == consts.SUCCESS:
                for each in val:

                    if each[0] not in denied:
                        print "ZipQuad has canceled reservation "+str(each[0])+" and will not be servicing this request."
                        denied.append(each[0])


            lastupdated = datetime.datetime.now()




main()