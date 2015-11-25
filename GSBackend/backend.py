from CloudConn import CloudConn
from Constants import constize
import datetime

consts = constize.Constant()
mav_id = consts.GRD_PY


class RQClass():
    def __init__(self):
        self.conn = CloudConn.CloudConn(mav_id)
        self.res_id = consts.UNINIT
        self.res_lat = consts.UNINIT
        self.res_lon = consts.UNINIT
        self.res_alt = consts.UNINIT
        self.res_dur = consts.UNINIT
        self.res_bearing = consts.UNINIT


    def isRes(self):
        if self.res_id == consts.UNINIT:
            return False
        return True

    def cancelReservation(self):
        if self.isRes():
            stat, val = self.conn.cancelreservation()
            if stat == consts.SUCCESS:
                self.res_id = consts.UNINIT
                return consts.SUCCESS, consts.SUCCESS
            return consts.DB_NOT_REACH, consts.DB_NOT_REACH
        return consts.FAIL_NOTINRES, consts.FAIL_NOTINRES

    def changeReservation(self, wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing):
        stat, val = self.conn.changereservation(wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing)
        if stat==consts.SUCCESS:
            self.res_lat            = wp_lat
            self.res_lon            = wp_lon
            self.res_alt            = wp_alt
            self.res_dur            = wp_dur
            self.res_bearing        = wp_bearing
            return consts.SUCCESS, consts.SUCCESS
        else:
            return stat,val

    def changeBearing(self,wp_bearing):
        stat, val = self.conn.changereservation(self.res_lat, self.res_lon, self.res_alt, self.res_dur, wp_bearing)
        if stat == consts.SUCCESS:
            self.res_bearing = wp_bearing
        return stat, val

    def changeAltitude(self, wp_alt):
        stat, val = self.conn.changereservation(self.res_lat, self.res_lon, wp_alt, self.res_dur, self.res_bearing)
        if stat == consts.SUCCESS:
            self.res_alt = wp_alt
        return stat, val

    def override(self, overridecode):
        return self.conn.createoverride(overridecode)

    def createreservation(self, wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing):
        stat, val = self.conn.createreservation(wp_lat, wp_lon, wp_alt, wp_dur, wp_bearing)
        if stat == consts.SUCCESS:
            self.res_id = val
        return stat, val
