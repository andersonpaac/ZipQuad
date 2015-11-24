#To Do

1. Setup software on RPi2
2. Setup huawei on RPi2
3. Setup simulator on RPi2
4. Make PX4 to RPI connections

allow pg to reconnect on a broken network

#Config CC

1. Setup UMTSKeeper


#Architecture
1.  Create table for airside updates.
2.  Create table for ground side reservations.



##Airside 


##FLIGHTS TABLE

mav_id-          ID of vehicle - {132: Simulator, 445:   Quad}
flt_id        ID of flight
flt_start           Local time of flight start
flt_end             Local time at end of flight
flt_status          Status of flight    
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

mav_time    location    status      resid



