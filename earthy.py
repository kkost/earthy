#!/usr/bin/env python 

import requests
import json
import os
from datetime import date, timedelta
import subprocess

img_format = "png"

today = date.today()
imgList = []
num_imgs = 0

while num_imgs < 22:
    todayf = today.strftime("%Y-%m-%d")
    today_json = json.loads(requests.get("http://epic.gsfc.nasa.gov/api/images.php?date=%s" % todayf).content)
    for entry in today_json:
        imgFile = entry[u'image'] + "." + img_format
        imgList.insert(0,imgFile)
        if not os.path.isfile(imgFile):
            print "Getting %s ..." % imgFile
            imgUrl = "http://epic.gsfc.nasa.gov/epic-archive/" + img_format + "/" + entry[u'image'] + "." + img_format
            newImg = requests.get(imgUrl, stream=True)
            with open(imgFile, 'wb') as f:
                for chunk in newImg.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
        num_imgs = num_imgs + 1
        if num_imgs >= 22:
            break
    if num_imgs >= 22:
        break
    today = today - timedelta(1)

convertcommand = ["/usr/bin/convert", "-delay", "100", "-resize", "750x750", "-bordercolor", "black", "-border", "0x292"] + imgList[::-1] + ["epic.gif"]
print(convertcommand)
subprocess.call(convertcommand)

