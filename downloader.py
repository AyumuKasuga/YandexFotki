#-*- coding: utf-8 -*-
from YandexFotki import YandexFotki
from Queue import Queue
import time
import threading
q=Queue()

threads=5

def qdownload():
    while True:
        try:
            args = q.get()
            print str(threading.currentThread().getName())+': '+str(args['filename'])+' downloading...'
            y.GetPhoto(args['link'], args['filename'], args['path'])
            print str(threading.currentThread().getName())+': '+str(args['filename'])+' downloaded'
        except q.Empty:
            print 'done!'
            break


y=YandexFotki('AyumuKasuga')
#print y.GetAlbums()
print 'Создание очереди...'
for e in y.GetAlbums():
    for k,v in list(y.GetAlbumPhotos(e['linkphotos']).iteritems()):
#        print k
#        y.GetPhoto(v, k, y.username+"/"+e['title'])
        q.put({'link' : v, 'filename' : k, 'path' : y.username+"/"+e['title']})
#        print "ok"

    print '['+str(q.qsize())+']['+str(e['title'])+']'

print "Очередь создана, длина очереди: "+str(q.qsize())

for x in range(threads):
    newthread=threading.Thread(target=qdownload, name='thread #'+str(x))
    newthread.start()

