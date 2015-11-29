import datetime
from Constants import constize
import ast
from CloudConn import CloudConn
def grounddaemon():
    served = []
    consts = constize.Constant()
    lastupdated = datetime.datetime.now() - datetime.timedelta(seconds=consts.SYNC_INTERVAL)
    cldconn = CloudConn.CloudConn(consts.GRD_DAEMON)
    while True:
        if datetime.datetime.now() >= lastupdated + datetime.timedelta(seconds=consts.SYNC_INTERVAL):
            try:
                fd = open(consts.LOG_FILE, "rb")
                data = fd.readlines()
                for each in data:
                    if len(each)>1:
                        dictuse = ast.literal_eval(each)
                        if dictuse['synctime'] not in served:
                            dat = datetime.datetime.strptime(dictuse['synctime'], "%m-%d-%y %I:%M %p")
                            now = datetime.datetime.now()
                            if dat <= now:
                                cldconn.createreservation(dictuse['lat'], dictuse['lon'], dictuse['alt'], dictuse['dur'], dictuse['bearing'])
                                served.append(dictuse['synctime'])
            except IOError:
                print "The required file doesn't exist yet\tWaiting for ground station to create this file"

            lastupdated = datetime.datetime.now()



grounddaemon()