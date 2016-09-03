#!/usr/bin/env python 

import argparse
import requests
import json
import os
from datetime import date, timedelta
import subprocess

parser = argparse.ArgumentParser(description='Fetch some cool stuff from DSCOVR\'s EPIC camera')
parser.add_argument('-f', '--format', help='source image format (default png)')
parser.add_argument('-o', '--output', help='latest or gif (default latest)')
parser.add_argument('-c', '--count', help='number of images to retrieve (default 1 if latest, 22 if gif)')
args = parser.parse_args()

if args.format:
    img_format = args.format
else:
    img_format = "png"

if args.output == "gif":
    max_imgs = 22

if args.count:
    max_imgs = args.count
elif args.output != "gif":
    max_imgs = 1

today = date.today()
imgList = []

num_imgs = 0
while num_imgs < max_imgs:
    todayf = today.strftime("%Y-%m-%d")
    today_json = json.loads(requests.get("http://epic.gsfc.nasa.gov/api/images.php?date=%s" % todayf).content)
    for entry in today_json:
        imgFile = entry[u'image'] + "." + img_format
        imgList.insert(0,imgFile)
        print imgFile
        if not os.path.isfile(imgFile):
            imgUrl = "http://epic.gsfc.nasa.gov/epic-archive/" + img_format + "/" + entry[u'image'] + "." + img_format
            newImg = requests.get(imgUrl, stream=True)
            with open(imgFile, 'wb') as f:
                for chunk in newImg.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
        num_imgs = num_imgs + 1
        if num_imgs >= max_imgs:
            break
    if num_imgs >= max_imgs:
        break
    today = today - timedelta(1)

if args.output == "gif":
    convertcommand = ["/usr/bin/convert", "-delay", "50", "-resize", "500x500"] + imgList[::-1] + ["earthy.gif"]
else:
    convertcommand = ["/usr/bin/convert"] + [imgList[0]] + ["epic.png"]
    
print(convertcommand)
subprocess.call(convertcommand)

