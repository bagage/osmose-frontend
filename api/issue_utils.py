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

import os
from .tool import tag2link
from modules.query import fixes_default

t2l = tag2link.tag2link(os.path.dirname(os.path.realpath(__file__)) + "/tool/tag2link_sources.xml")


def _get(db, err_id=None, uuid=None):
    columns_marker = ["markers.item", "markers.source_id", "markers.class", "markers.elems", "markers.fixes",
        "markers.lat", "markers.lon",
        "class.title", "markers.subtitle", "markers_counts.timestamp",
        "class.detail", "class.fix", "class.trap", "class.example", "class.source AS source_code", "class.resource",
        ]

    if err_id:
        sql = "SELECT uuid_to_bigint(markers.uuid) AS id, " + ",".join(columns_marker) + """
        FROM
            markers
            JOIN markers_counts ON
                markers.source_id = markers_counts.source_id AND
                markers.class = markers_counts.class
            JOIN class ON
                markers.item = class.item AND
                markers.class = class.class
        WHERE
            uuid_to_bigint(markers.uuid) = %s
        """
        db.execute(sql, (err_id, ))
    else:
        sql = "SELECT " + ",".join(columns_marker) + """
        FROM
            markers
            JOIN markers_counts ON
                markers.source_id = markers_counts.source_id AND
                markers.class = markers_counts.class
            JOIN class ON
                markers.item = class.item AND
                markers.class = class.class
        WHERE
            markers.uuid = %s
        """
        db.execute(sql, (uuid, ))

    marker = db.fetchone()

    if not marker:
        return None

    marker['fixes'] = fixes_default(marker['fixes'])
    marker['elems'] = list(map(lambda elem: dict(elem,
        type_long={'N':'node', 'W':'way', 'R':'relation'}[elem['type']],
    ), marker['elems'] or []))

    return marker


def _expand_tags(tags, links, short = False):
  t = []
  if short:
    for k in tags:
      t.append({"k": k})
  else:
    for (k, v) in sorted(tags.items()):
      if links and k in links:
        t.append({"k": k, "v": v, "vlink": links[k]})
      else:
        t.append({"k": k, "v": v})
  return t
