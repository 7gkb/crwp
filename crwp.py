#!/usr/bin/python
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import Tkinter as tk
import socket
import netifaces

hostname = socket.gethostname() 

root = tk.Tk()
widthscreen = root.winfo_screenwidth()
heightscreen = root.winfo_screenheight()
#print  widthscreen,"x",heightscreen
img = Image.new('RGB', (widthscreen, heightscreen), (0, 104, 252))
#img = Image.new('RGB', (widthscreen, heightscreen), (100, 100, 100))

step = 26
xstring = widthscreen - 300
ystring = 10

try:
    roomfile = open("/opt/crwp/.room")
    room = roomfile.read()
    stringtext4 = "Room Number: "+room
except IOError:
    stringtext4 = ""

draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("UbuntuMono-B.ttf", 16)

stringtext1 = "Computer Name: "+hostname
draw.text((xstring, ystring),stringtext1,(255,255,255),font=font)
ystring = ystring + step

devs = netifaces.interfaces()
for interface in devs:
  if (interface.find("veth") == -1 == interface.find("lo")):
    addrs = netifaces.ifaddresses(interface)
    try:
        mac = addrs[netifaces.AF_LINK][0]['addr']
        #ipaddrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET)[0]['addr']
        ipaddrs = addrs[netifaces.AF_INET][0]['addr']
    except TypeError:
        ipaddrs = "n/a"
        mac = "n/a"
    except KeyError:
        ipaddrs = "n/a"
        mac = "n/a"
    finally:
        stringtext2 = "IP-address: "+ipaddrs
        draw.text((xstring, ystring),stringtext2,(255,255,255),font=font)
        ystring = ystring + step
        stringtext3 = "MAC-address: "+mac
        draw.text((xstring, ystring),stringtext3,(255,255,255),font=font)
        ystring = ystring + step

draw.text((xstring, ystring),stringtext4,(255,255,255),font=font)

#font = ImageFont.truetype("UbuntuMono-B.ttf", 300)
#draw.text((40, 0),"+",(255,0,0),font=font)

#font = ImageFont.truetype("UbuntuMono-B.ttf", 200)
#draw.text((20, 20),"7",(0,0,255),font=font)

ystring = ystring + step
##position=(30,30)
try:
    logo = Image.open('/opt/crwp/logo.png')
    lwidth, lheight = logo.size
    width, height = img.size
    position=(width/2-lwidth/2, height/2-lheight/2)
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(img, (0,0))
    transparent.paste(logo, position, mask=logo)
#    transparent.show()
    wallpaper = transparent.convert('RGB')
    wallpaper.save('/opt/crwp/default_background.jpg')
except IOError:
#    img.show()
    wallpaper = img.convert('RGB')
    wallpaper.save('/opt/crwp/default_background.jpg')
    #pngimg.save("default_background.png", "png")
finally:
    print("OK")
