#-*- coding: utf-8 -*-

import urllib, os, sys
from BeautifulSoup import BeautifulSoup

class YandexFotki():
    def __init__(self, username):
        self.username=username
    def GetAlbums(self):
        srcalbums=urllib.urlopen('http://api-fotki.yandex.ru/api/users/'+self.username+'/albums/')
        srcxml=srcalbums.read()
        #создаем папочку
        os.makedirs(self.username)
        soup=BeautifulSoup(srcxml)
#        for entry in soup('entry'):
#            print str(entry)+"\n\n"
        self.album=[]
        for e in soup('entry'):
#            print e.title.string
#            e('link', {'rel' : 'self'})[0]['href']
#            e('link', {'rel' : 'photos'})[0]['href']
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
        urllib.urlretrieve(link, filename=path+"/"+filename, reporthook=self.DownloadStatus)
    def DownloadStatus(self, BlockAcquiredN, BlockAcquiredSize, TotalSize):
        sys.stdout.write('\r')
        downloaded=str(BlockAcquiredN*BlockAcquiredSize)
        sys.stdout.write("downloading: "+downloaded+"/"+str(TotalSize))
        sys.stdout.flush()
#        print "downloading: "+str(BlockAcquiredN)+" "+str(BlockAcquiredSize)+" "+str(TotalSize)

#y=YandexFotki('AyumuKasuga')
##print y.GetAlbums()
#for e in y.GetAlbums():
#    for k,v in list(y.GetAlbumPhotos(e['linkphotos']).iteritems()):
#        print k+" - "+v
#        y.GetPhoto(v, k, y.username+"/"+e['title'])
#        print "\n"
