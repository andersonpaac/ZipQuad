#To Do

1. Setup software on RPi2
2. Setup huawei on RPi2
3. Setup simulator on RPi2
4. Make PX4 to RPI connections

#Config CC

1. Setup UMTSKeeper


#Architecture
1.  Create table for airside updates.
2.  Create table for ground side reservations.



#Airside 


##FLIGHTS TABLE

mavid-          ID of vehicle - {132: Simulator, 445:   Quad}
flightid        ID of flight
start           Local time of flight start
end             Local time at end of flight
status          Status of flight    
                                    201 Success
                                    301 Override
                                    401 FAILSAFE

takeoffloc      GPS Coordinates of takeoff location
landloc         GPS Coordinates at land


flightid        mavid      start       end     status   takeoffloc      landloc

##FLT_ID

status  status of flight
                            101     In route to a reservation wp
                            201     Serving reservation 
                            301     Serving an override
                            401     Serving a failsafe
                            
resid       if status is 101 or 201    reservation id 
            if status is 401    
                                599 battery 
                                610 didn't take off

mavid   time    location    status      resid



