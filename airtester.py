from CloudConn import CloudConn
from Constants import constize
import time

cons = constize.Constant()

def main():
    cloudconn = CloudConn.CloudConn(cons.MAV_ID_SIM)
    while True:
        print cloudconn.getmissions()
        time.sleep(5)
main()

