import datetime
from Constants import constize
import ast
from CloudConn import CloudConn
def grounddaemon():
    served = []
    consts = constize.Constant()
    lastupdated = datetime.datetime.now()
    cldconn = CloudConn.CloudConn(consts.GRD_DAEMON)
    while True:
        if datetime.datetime.now() >= lastupdated + datetime.timedelta(seconds=consts.SYNC_INTERVAL):
            fd = open(consts.LOG_FILE, "rb")
            data = fd.readlines()
            for each in data:
                if len(each)>1:
                    dictuse = ast.literal_eval(each)
                    if dictuse['synctime'] not in served:
                        dat = datetime.datetime.strptime(dictuse['synctime'], "%m-%d-%y %I:%M %p")
                        print str(dat)
                        now = datetime.datetime.now()
                        if dat <= now:
                            cldconn.createreservation(dictuse['lat'], dictuse['lon'], dictuse['alt'], dictuse['dur'], dictuse['bearing'])
                            served.append(dictuse['synctime'])

            lastupdated = datetime.datetime.now()



grounddaemon()