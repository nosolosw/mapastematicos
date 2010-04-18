#!/usr/bin/env python

import sys
import web

from queriesdb import QueriesDB
from tests import db_config
from tests import report_data, map_data, tags
from tests import user

sys.path.append('/home/mapastematicos/pylibs/')
render = web.template.render('templates/')

urls = (
        '/', 'Index',
        '/map/(.+)', 'Map',
        '/tag/(.+)', 'Tag',
        '/search', 'Search'
)

app = web.application(urls, globals())

class Index:
    def GET(self):
        q = QueriesDB(db_config)
        resultset = q.getMoreViewedTags()
        return render.index(resultset)


class Map:
    def GET(self, id_map):
        q = QueriesDB(db_config)
        tagnames = q.getTags(id_map)
        title    = q.getTitle(id_map)
        vars     = [tagnames, title]

        if (title == None) and (tagnames == None):
            msg = "Lo sentimos, pero parece que no tenemos el mapa que nos pide."
            return render.notfound(msg)
        else:
            title = ""
            tagnames = {"None":"None"}
            return render.map(vars, id_map + ".png", id_map + "_thum.png")


class Tag:
    def GET(self, id_tag):
        q = QueriesDB(db_config)
        resultset = q.getResultsByTag(id_tag)
        if resultset == None:
            msg = "Lo sentimos, pero parece que no tenemos mapas con la etiqueta que nos pide."
            return render.notfound(msg)
        return render.search(resultset)


class Search:
    def GET(self):
        resultset = {"1": "oe",
                     "2": "eo"}
        if resultset == None:
            msg = "Lo sentimos, pero parece que no hemos encontrado nada como lo que nos pide."
            return render.notfound(msg)
        return render.search(resultset)



if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi

else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
