from pykml.factory import KML_ElementMaker as KML
from lxml import etree
from CloudConn import CloudConn
from Constants import constize
import datetime
cons = constize.Constant()
mav_id = cons.KML_PARSER
fname = "parser"
def main():
    kmlobj = KML.kml( KML.Document(KML.Style(KML.LabelStyle(KML.scale(6)),id="big_label")))
    data = '<?xml version="1.0" encoding="utf-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<name>Balloon with image</name>'
    cconn = CloudConn.CloudConn(mav_id)
    id = raw_input("flt_?")
    stat , vals = cconn.getallfromflt(int(id))
    counter = 0
    if stat == cons.SUCCESS:
        for each in vals:
            lat = float(each[0].split(",")[0].split("=")[1])
            lon = float(each[0].split(",")[1].split("=")[1])
            alt = float(each[0].split(",")[2].split("=")[1])
            kmlobj.Document.append(
            KML.Placemark(
                KML.name("ECE-445-DEMO"),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode('relativeToGround'),
                    KML.coordinates('{lon},{lat},{alt}'.format(
                            lon=lon,
                            lat=lat,
                            alt=alt,
                        ),
                    ))))
            #pm1 = KML.Placemark(KML.name(str(counter)),KML.Point(KML.coordinates(latlonstr)))
    dax = etree.tostring(etree.ElementTree(kmlobj),pretty_print=True)
    fd = open(fname+".kml", 'wb')
    fd.write(dax)
    fd.close()

main()