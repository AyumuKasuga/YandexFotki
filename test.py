#-*- coding: utf-8 -*-
from YandexFotki import YandexFotki

y=YandexFotki('AyumuKasuga')
#print y.GetAlbums()
for e in y.GetAlbums():
    for k,v in list(y.GetAlbumPhotos(e['linkphotos']).iteritems()):
        print k+" - "+v
        y.GetPhoto(v, k, y.username+"/"+e['title'])
        print "\n"
