#-*- coding: utf-8 -*-

import urllib, os, sys, httplib
from BeautifulSoup import BeautifulSoup

class YandexFotki():
    def __init__(self, username):
        self.username=username
    def GetAlbums(self):
        srcalbums=urllib.urlopen('http://api-fotki.yandex.ru/api/users/'+self.username+'/albums/')
        srcxml=srcalbums.read()
        #создаем папочку
        if os.path.exists(self.username) == False:
            os.makedirs(self.username)
        soup=BeautifulSoup(srcxml)
#        for entry in soup('entry'):
#            print str(entry)+"\n\n"
        self.album=[]
        for e in soup('entry'):
#            print e.title.string
#            e('link', {'rel' : 'self'})[0]['href']
#            e('link', {'rel' : 'photos'})[0]['href']
            if os.path.exists(self.username+"/"+e.title.string) == False:
                os.makedirs(self.username+"/"+e.title.string)
            
            
            self.album.append(
            {"title" : e.title.string,
            "linkalbum" : e('link', {'rel' : 'self'})[0]['href'],
            "linkphotos" : e('link', {'rel' : 'photos'})[0]['href']}
            )
        return self.album    
    def GetAlbumInfo(self):
        pass
    def GetAlbumPhotos(self, albumurl):
        srcalbum=urllib.urlopen(albumurl)
        srcxml=srcalbum.read()
        soup=BeautifulSoup(srcxml)
        photos={}
        for e in soup('entry'):
#            print e.title.string
#            print e('f:img', {'size' : 'orig'})[0]['href']
            photos[str(e.title.string)]=str(e('f:img', {'size' : 'orig'})[0]['href'])
        return photos
    def GetPhoto(self, link, filename, path):
        fullpath=path+"/"+filename.decode('utf-8')
        if os.path.exists(fullpath) == False:
#            urllib.urlretrieve(link, filename=fullpath, reporthook=self.DownloadStatus)
            urllib.urlretrieve(link, filename=fullpath)
    def DownloadStatus(self, BlockAcquiredN, BlockAcquiredSize, TotalSize):
        sys.stdout.write('\r')
        downloaded=str(BlockAcquiredN*BlockAcquiredSize)
        sys.stdout.write("downloading: "+self.HumanSize(BlockAcquiredN*BlockAcquiredSize)+"/"+self.HumanSize(TotalSize)+"\t\t")
        sys.stdout.flush()
    def HumanSize(self, size):
        if size < 524288:
            humansize=str(size)+' Bytes'
        elif size >= 524288 and size < 1048576:
            sizekb=round(float(size)/1024, 2)
            humansize=str(sizekb)+' Kb'
        elif size >= 1048576 and size < 536870912:
            sizemb=round(float(size)/1048576, 2)
            humansize=str(sizemb)+' Mb'
        elif size > 536870912:
            sizegb=round(float(size)/1073741824, 2)
            humansize=str(sizegb)+' Gb'
        return humansize
#        print "downloading: "+str(BlockAcquiredN)+" "+str(BlockAcquiredSize)+" "+str(TotalSize)

#y=YandexFotki('AyumuKasuga')
##print y.GetAlbums()
#for e in y.GetAlbums():
#    for k,v in list(y.GetAlbumPhotos(e['linkphotos']).iteritems()):
#        print k+" - "+v
#        y.GetPhoto(v, k, y.username+"/"+e['title'])
#        print "\n"
