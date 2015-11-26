__author__ = 'asc-mbp'

from Constants.constize import Constant
import datetime

class ZipQuad:

    def __init__(self):
        self.const = Constant()
        self.status = self.const.ZIP_WAIT_INST
        self.dest = ""
        self.resid = self.const.ZIP_WAIT_INST
        self.alt = self.const.CRUISE_ALT
        self.dur = self.const.UNINIT
        self.takeofftime = datetime.datetime.now()