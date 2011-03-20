#! /usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

###########################################################################
## database connection

import sys, os, cgi, Cookie, datetime
root_folder = os.environ["OSMOSE_ROOT"]
sys.path.append(root_folder)
from tools import utils

translate = utils.translator()._data
PgConn    = utils.get_dbconn()
PgCursor  = PgConn.cursor()

###########################################################################
## form fields

form = cgi.FieldStorage()

lat    = int(float(form.getvalue("lat", "0"))*1000000)
lon    = int(float(form.getvalue("lon", "0"))*1000000)
err_id = form.getvalue("item", "").split(",")
err_id = ",".join([str(int(x)) for x in err_id if x])
source = form.getvalue("source", "")
user   = form.getvalue("user", "")
zoom   = int(form.getvalue("zoom", "0"))
bbox   = form.getvalue("bbox", None).split(",")
minlon = int(1000000*float(bbox[0]))
minlat = int(1000000*float(bbox[1]))
maxlon = int(1000000*float(bbox[2]))
maxlat = int(1000000*float(bbox[3]))
bboxsql= "(dynpoi_marker.lat BETWEEN %d AND %d) AND (dynpoi_marker.lon BETWEEN %d and %d)"%(minlat, maxlat, minlon, maxlon)

###########################################################################
## page headers

print "Content-Type: text/plain; charset=utf-8"

cki = Cookie.SimpleCookie()
if os.environ.has_key('HTTP_COOKIE'):
    cki.load(os.environ['HTTP_COOKIE'])
cki["lastLat"] = form.getvalue("lat", "0")
cki["lastLat"]['expires'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d %b %Y %H:00:00 GMT")
cki["lastLat"]['path']    = '/'
cki["lastLon"] = form.getvalue("lon", "0")
cki["lastLon"]['expires'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d %b %Y %H:00:00 GMT")
cki["lastLon"]['path']    = '/'
cki["lastZoom"] = form.getvalue("zoom", "0")
cki["lastZoom"]['expires'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d %b %Y %H:00:00 GMT")
cki["lastZoom"]['path']    = '/'
cki["lastItem"] = form.getvalue("item", "")
cki["lastItem"]['expires'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d %b %Y %H:00:00 GMT")
cki["lastItem"]['path']    = '/'
if cki:
    print cki
            
###########################################################################
## data

print
print "\t".join(["lat", "lon", "marker_id", "icon", "iconSize", "iconOffset", "html"])

if (not user) and (not source) and (zoom < 8):
    sys.exit(0)
    
lang_def = utils.allowed_languages[0]
lang_cur = utils.get_language()
sqlbase  = """
SELECT dynpoi_marker.item,
       dynpoi_marker.source,
       dynpoi_marker.class,
       dynpoi_marker.elems,
       dynpoi_marker.subclass,
       dynpoi_marker.marker_id,
       dynpoi_marker.lat,
       dynpoi_marker.lon,
       dynpoi_class.title_%s as title_cur,
       dynpoi_class.title_%s as title_def,
       dynpoi_marker.subtitle_%s as subtitle_cur,
       dynpoi_marker.subtitle_%s as subtitle_def,
       dynpoi_marker.data
FROM dynpoi_marker
INNER JOIN dynpoi_class
  ON dynpoi_marker.source=dynpoi_class.source AND dynpoi_marker.class=dynpoi_class.class
WHERE %s
ORDER BY ABS(lat-%d)+ABS(lon-%d) ASC
LIMIT 100;"""

if source:
    sources = source.split(",")
    source2 = []
    for source in sources:
        source = source.split("-")
        if len(source)==1:
            source2.append("(dynpoi_marker.source=%d)"%int(source[0]))
        else:
            source2.append("(dynpoi_marker.source=%d AND dynpoi_marker.class=%d)"%(int(source[0]), int(source[1])))
    sources2 = " OR ".join(source2)
    where = "(%s) AND (%s)"%(sources2, bboxsql)
    sql =  sqlbase%(lang_cur, lang_def, lang_cur, lang_def, where, lat, lon)
elif user:
    sys.exit(0)
elif err_id:
    where = "(dynpoi_marker.item IN (%s)) AND (%s)"%(err_id,bboxsql)
    sql =  sqlbase%(lang_cur, lang_def, lang_cur, lang_def, where, lat, lon)
else:
    sys.exit(0)

###########################################################################
## sql querry

sql = sql.replace("--","+")
PgCursor.execute(sql)

#try:
#    open("/tmp/osmose-last.sql","w").write(sql+"\n")
#except:
#    pass

###########################################################################
## print results

for res in PgCursor.fetchall():
    lat       = str(float(res["lat"])/1000000)
    lon       = str(float(res["lon"])/1000000)
    error_id  = "%d-%d-%d-%s" % (res["source"], res["class"], res["subclass"], res["elems"])
    marker_id = "%d-%d-%d-%s-%d" % (res["source"], res["class"], res["subclass"], res["elems"], res["marker_id"])
    title     = res["title_cur"]    or res["title_cur"]    or "no title.."
    subtitle  = res["subtitle_cur"] or res["subtitle_cur"] or ""
    
    ############################################################
    ## build html

    html  = "<div style=\"float:right;margin-right:20;color:#EEEEEE;font-weight:bold;background-color:#AAAAAA;\" onclick=\"closeBubble('%s');\"><b>&nbsp;X&nbsp;</b></div>"%marker_id
    html += "<div class=\"bulle_err\">"
    html += "<b>%s</b><br>%s<br>"%(title, subtitle)
    html += "</div>"

    elems = []
    if res["data"]:
        for i in range(len(res["data"])/2):
            if res["data"][2*i].startswith("##"):
                elems.append([res["data"][2*i][2:], res["data"][2*i+1], {}])
            else:
                elems[-1][2][res["data"][2*i]] = res["data"][2*i+1]
    for e in elems:
        html += "<div class=\"bulle_elem\">"
        html += "<b><a class=\"bulle_elem\" target=\"_blank\" href=\"http://www.openstreetmap.org/browse/%s/%s\">%s %s</a></b>"%(e[0], e[1], e[0], e[1])
        html += " <a class=\"bulle_elem\" href=\"javascript:iFrameLoad('http://rawedit.openstreetmap.fr/edit/%s/%s');\">rawedit</a>"%(e[0], e[1])
        if e[0] == "relation" and "boundary" in e[2]:
            html += " <a class=\"bulle_elem\" target=\"_blank\" href=\"http://analyser.openstreetmap.fr/cgi-bin/index.py?relation=%s\">analyse1</a>"%e[1]
            html += " <a class=\"bulle_elem\" target=\"_blank\" href=\"http://osm3.crans.org/osmbin/analyse-relation?%s\">analyse2</a>"%e[1]
        if e[0] == "node":
            html += " <a class=\"bulle_elem\" href=\"http://localhost:8111/import?url=http://www.openstreetmap.org/api/0.6/node/"+e[1]+"\" target=\"hiddenIframe\">josm</a>"
        if e[0] == "way":
            html += " <a class=\"bulle_elem\" href=\"http://localhost:8111/import?url=http://www.openstreetmap.org/api/0.6/way/"+e[1]+"/full\" target=\"hiddenIframe\">josm</a>"
        if e[0] == "relation":
            html += " <a class=\"bulle_elem\" href=\"http://localhost:8111/import?url=http://www.openstreetmap.org/api/0.6/relation/"+e[1]+"/full\" target=\"hiddenIframe\">josm</a>"
        html += "<br>"
        for t in e[2].items():
            html += "<b>%s</b> = %s<br>"%(t[0], t[1])
        html += "</div>"

    ## bottom links
    html += "<a class=\"vert\" href=\"http://www.openstreetmap.org/?lat=%s&lon=%s&zoom=18\" target=\"_blank\">osmlink</a> "%(lat, lon)
    html += "<a class=\"vert\" href=\"http://www.openstreetmap.org/edit?lat=%s&lon=%s&zoom=18\" target=\"_blank\">potlatch</a> "%(lat, lon)
    html += "<a class=\"vert\" href=\"http://localhost:8111/load_and_zoom?left=%s&bottom=%s&right=%s&top=%s&select="%(bbox[0],bbox[1],bbox[2],bbox[3])+res["elems"].replace("_",",")+"\" target=\"hiddenIframe\">josm zone</a> "
    html += "<br>"
    html += "<b><u>%s :</u></b> "%translate[lang_cur][u"set_status"].encode("utf8")
    html += "<a onclick=\"setTimeout('pois.loadText();',2000);\" href=\"status.py?e=%s&s=done\" target=\"hiddenIframe\">%s</a> "%(error_id, translate[lang_cur][u"done"].encode("utf8"))
    html += "<a onclick=\"setTimeout('pois.loadText();',2000);\" href=\"status.py?e=%s&s=false\" target=\"hiddenIframe\">%s</a> "%(error_id, translate[lang_cur][u"false"].encode("utf8"))
    
    #html = html.replace("#CLOSE#",translate[lang][u"close"],1)
    #else:
    #    vals.append(u"'%s'"%utils.pg_escape(subtitle[:1000]+"[...]"))            
    
    html = "<font size=\"-1\">%s</font>"%html
    
    ##
    ############################################################

    marker   = "../markers/marker-b-%d.png" % (res["item"])
    print "\t".join([lat, lon, marker_id, marker, "17,33", "-8,-33", html])
    