#!/usr/bin/env python 

import requests
import json
import os.path
from datetime import datetime, date, timedelta

img_format = "png"

today = date.today()
imgList = []
num_imgs = 0

while num_imgs < 10:
    todayf = today.strftime("%Y-%m-%d")
    today_json = json.loads(requests.get("http://epic.gsfc.nasa.gov/api/images.php?date=%s" % todayf).content)
    print today
    for entry in today_json:
        imgList.insert(0,entry[u'image'])
        num_imgs = num_imgs + 1
        imgFile = entry[u'image'] + "." + img_format
        if not os.path.isfile(imgFile):
            print "Getting %s" % imgFile
            imgUrl = "http://epic.gsfc.nasa.gov/epic-archive/" + img_format + "/" + entry[u'image'] + "." + img_format
            newImg = requests.get(imgUrl, stream=True)
            with open(imgFile, 'wb') as f:
                for chunk in newImg.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)

    today = today - timedelta(1)

