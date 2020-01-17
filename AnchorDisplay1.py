#!/usr/bin/env python
import os
import json
import urllib2

#inkyWHAT library
from inky import InkyWHAT

inky_display = InkyWHAT("black")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img1 = Image.open("./Graphic.png")
#inky_display.set_image(img1)
#inky_display.show()

#img1 = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img1)

from font_fredoka_one import FredokaOne
font = ImageFont.truetype(FredokaOne, 25)

#Get data from signalk
g = urllib2.urlopen('http://demo.signalk.org/signalk/v1/api/')
#json_string = json.dumps(g.read())
signalkdata = json.loads(g.read())

#print signalkdata
#print "Sources:",signalkdata['sources']['nmeaFromFile']['II']['sentences']['MWV']

#Name = signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['name']
Name = "Black Dog"
UpdateTime = signalkdata['sources']['nmeaFromFile']['II']['sentences']['MWV']
MWVV = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['wind']['speedTrue']['value']))
MWVA = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['wind']['angleTrueWater']['value']))
DBT = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['depth']['belowTransducer']['value']))
VTG = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['navigation']['speedOverGround']['value']))


print "Name:",Name
print "UpdateTime:",UpdateTime
print "WMVV:",MWVV
print "MWVA:",MWVA
print "DBT:",DBT
print "VTG:",VTG

#close the file link
g.close()

#how big is the name?
w, h = font.getsize(Name)
x = (inky_display.WIDTH / 2) - (w / 2)
#y = (inky_display.HEIGHT / 2) - (h / 0.95)
y = 12
#Draw the name
draw.text((x, y), Name, inky_display.BLACK, font)

#Position the DBT
x = 212
y = 140
draw.text((x, y), DBT, inky_display.BLACK, font)

#y = (inky_display.HEIGHT / 2) - (h / 0.55)
#draw.text((x, y), UpdateTime, inky_display.BLACK, font)

#Position the MWVV
x = 212
y = 60
draw.text((x, y), MWVV, inky_display.BLACK, font)

#position the MWVA
x = 212
y = 96
draw.text((x, y), MWVA, inky_display.BLACK, font)

#position the VTG
x = 212
y = 184
draw.text((x, y), VTG, inky_display.BLACK, font)

#Set the image
inky_display.set_image(img1)
#Display the image
inky_display.show()






