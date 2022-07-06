#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import json
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

#epd2in13b_V3 RED COLOR
#Set output log level
logging.basicConfig(level=logging.DEBUG)
rel_path = "/home/pi/catfiles/catdata.json"

with open(rel_path) as json_file:
    data = json.load(json_file)
try:
    epd = epd2in13b_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    # Drawing on the Horizontal image
    logging.info("Drawing image")
    BlackImage = Image.new('1', (epd.height, epd.width), 255)
    RedImage = Image.new('1', (epd.height, epd.width), 255)
    drawBlack = ImageDraw.Draw(BlackImage)
    drawRed = ImageDraw.Draw(RedImage)
    #draw.rectangle([(0,0),(50,50)],outline = 0)

    
    xzero = 10
    xstart = xzero+60
    xdiff = 45
    yzero = 6
    ystart = 18 + yzero
    ydiff = 18

    if (data['feed1']['deviation'] < 6) and (data['feed2']['deviation'] <6) and (data['feed3']['deviation'] <6):

        drawBlack.text((xstart, yzero), "06:00", font = font15, fill = 0)
        drawBlack.text((xstart+xdiff, yzero), "18:00", font = font15, fill = 0)
        drawBlack.text((xstart+xdiff*2, yzero), "22:00", font = font15, fill = 0)

        
        drawBlack.text((xzero, yzero), str(data['date calculated']), font = font15, fill = 0)
        drawBlack.text((xzero, ystart), "given", font = font15, fill = 0)
        drawBlack.text((xzero, ystart+ydiff), "wanted", font = font15, fill = 0)
        drawBlack.text((xzero, ystart+ydiff*2), "diff", font = font15, fill = 0)
        drawBlack.text((xzero, ystart+ydiff*3), "time", font = font15, fill = 0)
        

        xoffset = 10
        xstart = xstart + xoffset

        drawBlack.text((xstart, ystart), str(data['feed1']['amountgiven']), font = font15, fill = 0)
        drawBlack.text((xstart, ystart+ydiff), str(data['feed1']['wanted']), font = font15, fill = 0)
        drawBlack.text((xstart, ystart+ydiff*2), str(data['feed1']['deviation']), font = font15, fill = 0)
        drawBlack.text((xstart, ystart+ydiff*3), str(data['feed1']['time']), font = font15, fill = 0)

        drawBlack.text((xstart+xdiff, ystart), str(data['feed2']['amountgiven']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff, ystart+ydiff), str(data['feed2']['wanted']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff, ystart+ydiff*2), str(data['feed2']['deviation']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff, ystart+ydiff*3), str(data['feed2']['time']), font = font15, fill = 0)

        drawBlack.text((xstart+xdiff*2, ystart), str(data['feed3']['amountgiven']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff*2, ystart+ydiff), str(data['feed3']['wanted']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff*2, ystart+ydiff*2), str(data['feed3']['deviation']), font = font15, fill = 0)
        drawBlack.text((xstart+xdiff*2, ystart+ydiff*3), str(data['feed3']['time']), font = font15, fill = 0)

        xend = 250
        yend = 122

        xzeroline = xzero-5
        xstart = xzeroline + 60
        xdiffline = xdiff
        xendline = xstart + xdiffline*3

        yzeroline = yzero-3   
        ystart = yzeroline + 21
        ydiffline = ydiff
        yendline = ystart + ydiffline*4
        
        #horizontal lines
        drawRed.line([(xzeroline,yzeroline),(xendline,yzeroline)], fill = 0,width = 2)
        drawRed.line([(xzeroline,ystart),(xendline,ystart)], fill = 0,width = 1)
        drawRed.line([(xzeroline,ystart + ydiffline),(xendline,ystart + ydiffline)], fill = 0,width = 1)
        drawRed.line([(xzeroline,ystart + ydiffline*2),(xendline,ystart + ydiffline*2)], fill = 0,width = 1)
        drawRed.line([(xzeroline,ystart+ ydiffline*3),(xendline,ystart + ydiffline*3)], fill = 0,width = 1)
        drawRed.line([(xzeroline,ystart + ydiffline*4),(xendline,ystart +ydiffline*4)], fill = 0,width = 2)

        #vertical lines

        drawRed.line([(xzeroline,yzeroline),(xzeroline,yendline)], fill = 0,width = 2)
        drawRed.line([(xstart,yzeroline),(xstart,yendline)], fill = 0,width = 1)
        drawRed.line([(xstart + xdiffline,yzeroline),(xstart + xdiffline,yendline)], fill = 0,width = 1)
        drawRed.line([(xstart + xdiffline*2,yzeroline),(xstart + xdiffline*2,yendline)], fill = 0,width = 1)
        drawRed.line([(xstart + xdiffline*3,yzeroline),(xstart + xdiffline*3,yendline)], fill = 0,width = 2)
    
    else:
        drawRed.text((10, 30), "ERROR SCALE!", font = font30, fill = 0)

    #outerbox
    
    epd.display(epd.getbuffer(BlackImage), epd.getbuffer(RedImage))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13d.epdconfig.module_exit()
    exit()