
import ephem
import os
import re
from datetime import datetime, timedelta
import shutil
import pause
import time
import logging

import subprocess
osdate_read =  subprocess.Popen("date", shell=True, stdout=subprocess.PIPE).stdout
osdate =  osdate_read.read()

o = ephem.Observer()
# for some reason o.lat and o.long if initalized as a string it expects degrees, but if initalized as a float it appears to expect radians
o.lat, o.long = os.environ.get("LATITUDE"), os.environ.get("LONGITUDE")
sun = ephem.Sun()

input_root_path = os.environ.get("INPUT_ROOT")
capture_dirs = os.listdir(input_root_path)
timelapse_dirs = [timelapse_dirs for timelapse_dirs in capture_dirs if "_timelapse" in timelapse_dirs]
output_root_path = os.environ.get("OUTPUT_ROOT")

numeric_level = getattr(logging, os.environ.get("LOGLEVEL").upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

logging.info("Longitue is: " + str(float(o.long)) +" Latitide: " + str(float(o.lat)) + " root path is: " + input_root_path + " logging level is " + str(numeric_level))
logging.debug("datetime.now: " + str(datetime.now()) + " ephem.localtime(o.next_transit(sun)): " + str(ephem.localtime(o.next_transit(sun))) + " os.system(\"date\"): " + str(osdate) )

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

while True:
    for camera in timelapse_dirs:
        noon_cam_path = str(output_root_path) + str(camera) + "_noon/"
        isExist = os.path.exists(noon_cam_path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(noon_cam_path)
        days = (os.listdir(input_root_path + "/" + camera))
        for day in days:
            logging.debug("local time of solar noon on " + str(day) + " is " + str(ephem.localtime(o.next_transit(sun,start=day))))
            pictures = (os.listdir(input_root_path + "/" + camera + "/" + day))
            if(len(pictures)>10):
                closest_pic = closest([ datetime.strptime(picture_date,"%Y-%m-%dT%H-%M-%S.jpg") for picture_date in pictures],ephem.localtime(o.next_transit(sun,start=day)))
                regex = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2})"
                subst = "\\1T\\2-\\3-\\4.jpg"
                time_diff = (closest_pic - ephem.localtime(o.next_transit(sun,start=day))).total_seconds()
                
                pic_filename = (re.sub(regex,subst,str(closest_pic)))
                pic_path = str(input_root_path + "/" + camera + "/" + day + "/" +pic_filename)
                logging.debug("Pic path is: " + pic_path +  " difference is: " + str(time_diff))
                if(time_diff < 60):
                    if not (os.path.exists(noon_cam_path + pic_filename)):
                        #TODO: I belelvie this overwrites, I should modify to not copy  if already exsists
                        shutil.copy2(pic_path,noon_cam_path + pic_filename)
                        logging.info("found a close enough picture copying: " + pic_path + " to: " + noon_cam_path + pic_filename)
                    #else: 
                        logging.debug("no picture close enough, not copying " + noon_cam_path + pic_filename)
    pause_until = datetime.now() + timedelta(hours=23)
    logging.info(pause_until)
    pause.until(pause_until)
    
