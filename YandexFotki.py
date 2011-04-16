#-*- coding: utf-8 -*-

# Документация по API Яндекс фоток: http://api.yandex.ru/fotki/doc/concepts/About.xml
# Модуль содержит только основные функции необходимые для скачивания фотографий и альбомов (альбомы должны быть открыты для людей)

import urllib, os, sys, httplib
from BeautifulSoup import BeautifulSoup

class YandexFotki():
    def __init__(self, username):
        self.username=username
    def GetAlbums(self):
        '''Забирает альбомы пользователя
        Возвращает словарь:
        title - название альбома,
        linkalbum - ссылка на альбом
        linkphotos - ссылка на фоточки альбома
        '''
        srcalbums=urllib.urlopen('http://api-fotki.yandex.ru/api/users/'+self.username+'/albums/')
        srcxml=srcalbums.read()
        if os.path.exists(self.username) == False:
            os.makedirs(self.username)
        soup=BeautifulSoup(srcxml)
        self.album=[]
        for e in soup('entry'):
            if os.path.exists(self.username+"/"+e.title.string) == False:
                os.makedirs(self.username+"/"+e.title.string)
            
            
            self.album.append(
            {"title" : e.title.string,
            "linkalbum" : e('link', {'rel' : 'self'})[0]['href'],
            "linkphotos" : e('link', {'rel' : 'photos'})[0]['href']}
            )
        return self.album    
    def GetAlbumInfo(self):
        '''Возвращает информацию об альбоме (не реализовано)'''
        pass
    def GetAlbumPhotos(self, albumurl):
        '''Функция забирает список фоточек альбома'''
        srcalbum=urllib.urlopen(albumurl)
        srcxml=srcalbum.read()
        soup=BeautifulSoup(srcxml)
        photos={}
        for e in soup('entry'):
            photos[str(e.title.string)]=str(e('f:img', {'size' : 'orig'})[0]['href'])
        return photos
    def GetPhoto(self, link, filename, path):
        '''Скачиваем и сохраняем фоточку'''
        fullpath=path+"/"+filename.decode('utf-8')
        if os.path.exists(fullpath) == False:
#           Используйте эту строку, вместо следущей, чтобы видеть прогресс скачивания
#            urllib.urlretrieve(link, filename=fullpath, reporthook=self.DownloadStatus)
            urllib.urlretrieve(link, filename=fullpath)
    def DownloadStatus(self, BlockAcquiredN, BlockAcquiredSize, TotalSize):
        '''выводит статус закачки текущей фотографии (фигово работает при многопоточности)'''
        sys.stdout.write('\r')
        downloaded=str(BlockAcquiredN*BlockAcquiredSize)
        sys.stdout.write("downloading: "+self.HumanSize(BlockAcquiredN*BlockAcquiredSize)+"/"+self.HumanSize(TotalSize)+"\t\t")
        sys.stdout.flush()
    def HumanSize(self, size):
        '''человечиский размеры скачиваемых файлов'''
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

