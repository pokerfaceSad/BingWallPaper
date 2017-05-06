#coding=utf8

import urllib2
import json
import os
import win32api
import win32con
import win32gui
import Image
import time

path  = 'D:/bingPic/'
no = 0

def getNo():
    pathDir = os.listdir(path)
    global no
    no = len(pathDir)
    no = no-1 if no!=0 else 0
def downloadBingPic():
    url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=1&n=1&nc=1491749880722&pid=hp'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    
    data = json.loads(response.read())
    
    url = 'http://cn.bing.com'+data['images'][0]['url']
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    global no
    no+=1
    with open(path + "%d.jpg" % no , "wb") as f:
        f.write(response.read())
def set_wallpaper_from_bmp(bmp_path):  
    #打开指定注册表路径  
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
    #最后的参数:2拉伸,0居中,6适应,10填充,0平铺  
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
    #最后的参数:1表示平铺,拉伸居中等都是0  
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
    #刷新桌面  
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(img_path):  
    #把图片格式统一转换成bmp格式,并放在源图片的同一目录  
    img_dir = os.path.dirname(img_path)  
    bmpImage = Image.open(img_path)  
    new_bmp_path = os.path.join(img_dir,'wallpaper.bmp')  
    bmpImage.save(new_bmp_path, "BMP")  
    set_wallpaper_from_bmp(new_bmp_path)
'''
    获取最新图片信息，判断是否今日已下载过
'''    
def isTodayDownloaded(no):
    if no==0:
        return False
    statinfo=os.stat("D:/bingPic/%d.jpg" % no)
    ctime = time.localtime(statinfo.st_ctime)
    ltime =  time.localtime()
    if ctime.tm_yday == ltime.tm_yday and ctime.tm_year == ltime.tm_year:
        return True
    return False

if __name__ == '__main__':
    
    getNo()  
    if not isTodayDownloaded(no):
        print 'downloading...'
        downloadBingPic()
    else:
        no = no-1 if no!=1 else 1
    print 'setting...'
    set_wallpaper(path+'%d.jpg' % no)
    print 'successfully!'
