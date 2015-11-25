__author__ = 'asc-mbp'

from Constants.constize import Constant

class ZipQuad:

    def __init__(self):
        self.const = Constant()
        self.status = self.const.ZIP_WAIT_INST
        self.dest = ""
        self.resid = self.const.ZIP_WAIT_INST
