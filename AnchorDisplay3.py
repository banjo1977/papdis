#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import os
import json
import urllib2
#inkyWHAT library
from inky import InkyWHAT
from datetime import datetime

#Setup display
inky_display = InkyWHAT("black")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

#Define function to convert from decimal degrees to DM.MMM for Lat and LON with padded zero for LON.
import math

def deg_to_dms_lat(deg, type='lat'):
        decimals, number = math.modf(deg)
        d = int(number)
        m = decimals * 60
        compass = {
            'lat': ('N','S'),
            'lon': ('E','W')
        }
        compass_str = compass[type][0 if d >= 0 else 1]
        return '{} {}\' {}'.format(abs(d), abs(m), compass_str)

def deg_to_dms_lon(deg, type='lon'):
        decimals, number = math.modf(deg)
        d = int(number)
        dz = str((abs(int(number)))).zfill(3)
        m = decimals * 60
        compass = {
            'lat': ('N','S'),
            'lon': ('E','W')
        }
        compass_str = compass[type][0 if d >= 0 else 1]
        return '{} {}\' {}'.format(dz, abs(m), compass_str)

#Use this to load a background image.
#img1 = Image.open("./Graphic.png")

#Use this line to use a blank slate.
img1 = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img1)

#Define the font sizes
font = ImageFont.truetype('FreeSansBold.ttf', 25)
font_small = ImageFont.truetype('FreeSansBold.ttf', 14)

#Get data from signalk in a JSON string
g = urllib2.urlopen('http://demo.signalk.org/signalk/v1/api/')
signalkdata = json.loads(g.read())

#Break out the information we need from the JSON string
Name = signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['name']
UpdateTime = signalkdata['sources']['nmeaFromFile']['II']['sentences']['MWV']
MWVV = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['wind']['speedTrue']['value']))
#MWVV = str(34)
MWVA = str(int(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['wind']['angleTrueWater']['value']))
MWVA = str(45)
DBT = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['environment']['depth']['belowTransducer']['value']))
VTG = str(round(signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['navigation']['speedOverGround']['value']))
GLLLON=signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['navigation']['position']['value']['longitude']
GLLLAT=signalkdata['vessels']['urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d']['navigation']['position']['value']['latitude']


#Diagnostic string printing - BLOCK 1
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
y = 12
#Draw the name
draw.text((x, y), Name, inky_display.BLACK, font)

#Position the DBT
x = 175
y = 140
draw.text((x, y), DBT, inky_display.BLACK, font)
draw.text((x+2, y+22), "Depth", inky_display.BLACK, font_small)

#position the VTG
x = 175
y = 184
draw.text((x, y), VTG, inky_display.BLACK, font)
draw.text((x+2, y+22), "VMG", inky_display.BLACK, font_small)

########GRAPHIC DISPLAY OF MWVV ################
#Draw the MWVV dial
#determne the MWVV-dial-angle
#multiplier of 7.2 makes 50kts of wind 360 degrees - 50kts at top of scale, 25kts at bottom
MWVVdialangle=((float(MWVV)*7)-90)
print "MWVV Dial Angle:",MWVVdialangle
#draw the MWVV dial.
draw.pieslice((275,54,380,150),-90,270,inky_display.RED,inky_display.BLACK,3)
draw.pieslice((278,57,377,147),-90,MWVVdialangle,inky_display.BLACK,inky_display.WHITE,1)

#Position the MWVV
w, h = font.getsize(MWVV)
x = (325) - (w / 2)
y = 89
#Draw a white box under MWVV
draw.rectangle(((x-2),(y-1),(x+w+2),(y+h+3)),inky_display.WHITE,5)
#draw the MWVV inside the dial
draw.text((x,y), MWVV, inky_display.BLACK, font)

#draw scale to suit x7.2 multiplier
label = "0"
w, h = font_small.getsize(label)
x = (325) - (w / 2)
draw.text((x,40),label, inky_display.BLACK, font_small)
label = "25"
w, h = font_small.getsize(label)
x = (325) - (w / 2)
draw.text((x,151),label, inky_display.BLACK, font_small)
label = "15"
draw.text((385,95),label, inky_display.BLACK, font_small)
label = "38"
draw.text((255,95),label, inky_display.BLACK, font_small)



########GRAPHIC DISPLAY OF MWVA ################
#Draw the MWVA dial
#determne the MWVVAdial-angle
MWVAdialangle=(int(MWVA)-90)
print "MWVA Dial Angle:",MWVAdialangle
#draw the MWVA dial.
draw.pieslice((20,54,125,150),-90,270,inky_display.RED,inky_display.BLACK,3)
draw.pieslice((23,57,122,147),(MWVAdialangle-3),(MWVAdialangle+3),inky_display.BLACK,inky_display.BLACK,1)


#Derive the text for the MWVA box in the dial (P, S, A)
if (int(MWVA)) < 0: MWVAflag="P"
elif (int(MWVA)) >= 1: MWVAflag="S"
elif (int(MWVA)) == 0: MWVAflag=""
MWVAtext=(MWVAflag+str(abs(int(MWVA))))
print "MWVA Text:", MWVAtext

#Position the MWVA text
w, h = font.getsize(MWVAtext)
x = (72) - (w / 2)
y = 89
#Draw a white box under MWVV
draw.rectangle(((x-2),(y-1),(x+w+2),(y+h+3)),inky_display.WHITE,5)
#draw the MWVA inside the dial
draw.text((x,y), MWVAtext, inky_display.BLACK, font)

#draw scale
label = "0"
w, h = font_small.getsize(label)
x = (73) - (w / 2)
draw.text((x,40),label, inky_display.BLACK, font_small)
label = "180"
w, h = font_small.getsize(label)
x = (73) - (w / 2)
draw.text((x,151),label, inky_display.BLACK, font_small)
label = "90"
draw.text((3,95),label, inky_display.BLACK, font_small)
label = "90"
draw.text((130,95),label, inky_display.BLACK, font_small)


##########BELOW THE LINE BIT###############
#DIAGNOSTIC STRING PRINT - BLOCK 2
print "GLL:",GLLLAT," ",GLLLON
print deg_to_dms_lat(GLLLAT)
print deg_to_dms_lon(GLLLON)

#Position the LAT
x = 136
y = 270
draw.text((x, y), deg_to_dms_lat(GLLLAT), inky_display.BLACK, font_small)
#Position the LON
x = 134
y = 285
draw.text((x, y), deg_to_dms_lon(GLLLON), inky_display.BLACK, font_small)

#Position the current date and time
now=datetime.now()
dt_string = now.strftime("%d/%m/%Y - %H:%M:%SZ")

x = 253
y = 285
draw.text((x, y), dt_string, inky_display.BLACK, font_small)

###############DISPLAY IT#####################
#Set the image
inky_display.set_image(img1)
#Display the image
inky_display.show()






