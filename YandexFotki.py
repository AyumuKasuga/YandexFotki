#-*- coding: utf-8 -*-

# Документация по API Яндекс фоток: http://api.yandex.ru/fotki/doc/concepts/About.xml
# Модуль содержит только основные функции необходимые для скачивания фотографий и альбомов (альбомы должны быть открыты для людей)

import urllib
import os
import sys
import httplib
import re
import httplib
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
# BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)


class YandexFotki():

    '''содержит основные функции для работы (скачивания фоточек) с API яндекс фоток'''

    def __init__(self, username):
        self.username = username
        self.album = []

    def PrepareAlbumsNames(self):
        """ Меняет имена альбомам и создает дирректории """
        self.GetAlbums()
        buff = []
        for album in self.album:
            # Копируем элемент. Иначе получим задваивание имен при рекурсии
            a = dict(album)
            a['title'] = self.GetAlbumsName(album)
            buff.append(a)
            albumpath = self.username + "/" + a['title']
            if not os.path.exists(albumpath):
                os.makedirs(albumpath)
        self.album = buff

    def GetAlbumsName(self, album, buff=''):
        """ Составляет название альбома использую полную иерархию альбомов """
        if buff:
            name = '%s/%s' % (album['title'], buff)
        else:
            name = album['title']
        if 'linkparent' in album:
            # Ищем альбом-родитель
            parentAlbum = [x for x in self.album if album['linkparent'] == x['linkalbum']][0]
            return self.GetAlbumsName(parentAlbum, name)
        return name

    def GetAlbums(self, nexturl=''):
        '''Забирает альбомы пользователя
        Возвращает словарь:
        title - название альбома,
        linkalbum - ссылка на альбом
        linkphotos - ссылка на фоточки альбом
        linkparent - ссылка на родительский альбом
        '''
        try:
            if not nexturl:
                # Если нет nexturl и что-то есть в albums - значит альбомы уже выкачены
                if self.album:
                    return self.album
                srcalbums = urllib.urlopen(
                    'http://api-fotki.yandex.ru/api/users/' + self.username + '/albums/')
            else:
                srcalbums = urllib.urlopen(nexturl)
        except:
            print "Что-то пошло не так! возможно, неверное имя пользователя или что-то еще..."
        srcxml = srcalbums.read()
        if os.path.exists(self.username) == False:
            os.makedirs(self.username)
        soup = BeautifulSoup(srcxml)
        for e in soup('entry'):
            #if os.path.exists(self.username + "/" + e.title.string) == False:
            #    os.makedirs(self.username + "/" + e.title.string)
            album = {"title": e.title.string,
                "linkalbum": e('link', {'rel': 'self'})[0]['href'],
                "linkphotos": e('link', {'rel': 'photos'})[0]['href']}
            if e('link', {'rel': 'album'}):
                album['linkparent'] = e('link', {'rel': 'album'})[0]['href']
            self.album.append(album)

        if soup('link', {'rel': 'next'}):
            self.GetAlbums(soup('link', {'rel': 'next'})[0]['href'])

        return self.album

    def GetAlbumInfo(self):
        '''Возвращает информацию об альбоме (не реализовано)'''
        pass

    def GetAlbumPhotos(self, albumurl, buff=[]):
        '''Функция забирает список фоточек альбома'''
        srcalbum = urllib.urlopen(albumurl)
        srcxml = srcalbum.read()
        soup = BeautifulSoup(srcxml)
        photos = {}
        for e in soup('entry'):
            photos[str(e.title.string)] = str(
                e('f:img', {'size': 'orig'})[0]['href'])
        if soup('link', {'rel': 'next'}):
            photos = self.GetAlbumPhotos(soup('link', {"rel": "next"})[0]['href'], photos)
        photos.update(buff)
        return photos

    def GetPhoto(self, link, filename, path):
        '''Скачиваем и сохраняем фоточку'''
        filename = str(filename)
        pattern = r"(\.jpg|\.jpeg|\.bmp|\.BMP|\.gif|\.GIF|\.png|\.PNG|\.tiff|\.TIFF|\.JPG|\.JPEG)"
        cpattern = re.compile(pattern)
        typefile = cpattern.findall(filename)
        if len(typefile) < 1:
            filetype = self.GetFileType(link)
            filename = filename + str(filetype)
        fullpath = path + "/" + filename.decode('utf-8')
        print fullpath
        if os.path.exists(fullpath) == False:
#           Используйте эту строку, вместо следущей, чтобы видеть прогресс скачивания
#            urllib.urlretrieve(link, filename=fullpath, reporthook=self.DownloadStatus)
            urllib.urlretrieve(link, filename=fullpath)
            downloading = True
        else:
            downloading = False
        filesize = os.path.getsize(fullpath)
        if downloading == True:
            return {'filesize': self.HumanSize(filesize), 'exists': False}
        else:
            return {'filesize': self.HumanSize(filesize), 'exists': True}

    def GetFileType(self, link):
        '''Получение типа файла (для файлов без расширений)'''
        o = urlparse(link)
        conn = httplib.HTTPConnection(o.netloc)
        conn.request("HEAD", o.path)
        res = conn.getresponse()
        headers = res.getheaders()
        head = {}
        for k, v in headers:
            head[k] = v
        contenttype = head['content-type']
        types = {
            'image/jpeg': '.jpg',
            'image/gif': '.gif',
            'image/tiff': '.tiff',
            'image/bmp': '.bmp',
            'image/png': '.png'
        }
        return types[contenttype]

    def DownloadStatus(self, BlockAcquiredN, BlockAcquiredSize, TotalSize):
        '''выводит статус закачки текущей фотографии (фигово работает при многопоточности)'''
        sys.stdout.write('\r')
        downloaded = str(BlockAcquiredN * BlockAcquiredSize)
        sys.stdout.write("downloading: " + self.HumanSize(
            BlockAcquiredN * BlockAcquiredSize) + "/" + self.HumanSize(TotalSize) + "\t\t")
        sys.stdout.flush()

    def HumanSize(self, size):
        '''человеческий размеры скачиваемых файлов'''
        if size < 524288:
            humansize = str(size) + ' Bytes'
        elif size >= 524288 and size < 1048576:
            sizekb = round(float(size) / 1024, 2)
            humansize = str(sizekb) + ' Kb'
        elif size >= 1048576 and size < 536870912:
            sizemb = round(float(size) / 1048576, 2)
            humansize = str(sizemb) + ' Mb'
        elif size > 536870912:
            sizegb = round(float(size) / 1073741824, 2)
            humansize = str(sizegb) + ' Gb'
        return humansize
