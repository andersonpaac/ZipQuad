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
class CloudConn:

    #Make connection
    def __init__(self):



    #Should send location, status(mission, failsafe, available, RTH), battery, velocity, RESSTART
    def updateCloud(self):


    #Remove message from queue
    def checkcloud(self):