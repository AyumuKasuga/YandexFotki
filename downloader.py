#-*- coding: utf-8 -*-
from YandexFotki import YandexFotki
from Queue import Queue
import time, sys, os
import threading
argv=sys.argv
#print argv[1]
try:
    username=argv[1]
except IndexError:
    print "Не указано имя пользователя!"
    sys.exit()

try:
    threads=int(argv[2])
except IndexError:
    print "Не указано количество потоков, используем значение по умолчанию [5]"
    threads=5


q=Queue()
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


y=YandexFotki(username)
#print y.GetAlbums()
print 'Создание очереди...'
for e in y.GetAlbums():
    for k,v in list(y.GetAlbumPhotos(e['linkphotos']).iteritems()):
#        print k
#        y.GetPhoto(v, k, y.username+"/"+e['title'])
        q.put({'link' : v, 'filename' : k, 'path' : y.username+"/"+e['title']})
#        print "ok"

    print '['+str(q.qsize())+']['+str(e['title'])+']'

if q.qsize() == 0:
    print "Очередь пуста, наверное вы неправильно указали имя пользователя, или у него нет альбомов доступных для скачивания"
    os.removedirs(username)
    sys.exit()

print "Очередь создана, длина очереди: "+str(q.qsize())

for x in range(threads):
    newthread=threading.Thread(target=qdownload, name='thread #'+str(x))
    newthread.start()

