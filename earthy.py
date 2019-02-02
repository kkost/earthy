#!/usr/bin/env python3.7 

import fire
import urllib.request
import shutil
import json
import os
from datetime import date, timedelta

OUTPUT_PATH = "/tmp/"
IMAGE_LIST_URL_BASE = "http://epic.gsfc.nasa.gov/api/images.php?date="
IMAGE_URL_BASE = "http://epic.gsfc.nasa.gov/epic-archive/"
IMAGE_FORMAT = "png"

class Epic(object):
    def __image_list(self, idate):
        return json.loads(urllib.request.urlopen(IMAGE_LIST_URL_BASE + idate.strftime("%Y-%m-%d")).read().decode('utf-8'))

    def __get_file(self, url, out_file):
        print("Getting {}".format(url))
        with urllib.request.urlopen(url) as response, open(out_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Wrote {}".format(out_file))

    def get_latest(self):
        today = date.today()

        while True:
            print("Checking images for {}".format(today))

            if not self.__image_list(today):
                today = today - timedelta(1)
                continue

            img_name = self.__image_list(today)[-1][u'image'] + "." + IMAGE_FORMAT
            out_file = OUTPUT_PATH + img_name

            if not os.path.isfile(out_file):
                url = IMAGE_URL_BASE + IMAGE_FORMAT + "/" + img_name
                self.__get_file(url, out_file)
            else:
                print("{} exists".format(out_file))

            break


if __name__ == '__main__':
    fire.Fire(Epic)
