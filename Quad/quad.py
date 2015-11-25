__author__ = 'asc-mbp'

from Constants.constize import Constant

class ZipQuad:

    def __init__(self):
        self.const = Constant()
        self.status = self.const.AWAITING_INST
        self.dest = ""
