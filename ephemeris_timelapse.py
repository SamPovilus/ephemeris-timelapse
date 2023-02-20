
import ephem
import os
import re
import datetime
import shutil
from IPython.display import Image
o = ephem.Observer()
o.lat, o.long = '39.98', '0.0'
sun = ephem.Sun()

root_path = "/timelapse/FVSYkiwp2G"
capture_dirs = os.listdir(root_path)
timelapse_dirs = [timelapse_dirs for timelapse_dirs in capture_dirs if "_timelapse" in timelapse_dirs]

print(timelapse_dirs)

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

for camera in timelapse_dirs:
    noon_cam_path = "/timelapse/" + str(camera) + "_noon/"
    isExist = os.path.exists(noon_cam_path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(noon_cam_path)
    days = (os.listdir(root_path + "/" + camera))
    for day in days:
        print(ephem.localtime(o.next_transit(sun,start=day)))
        pictures = (os.listdir(root_path + "/" + camera + "/" + day))
        #print(pictures)
        if(len(pictures)>10):
            closest_pic = closest([ datetime.datetime.strptime(picture_date,"%Y-%m-%dT%H-%M-%S.jpg") for picture_date in pictures],ephem.localtime(o.next_transit(sun,start=day)))
            regex = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2})"
            subst = "\\1T\\2-\\3-\\4.jpg"
            time_diff = (closest_pic - ephem.localtime(o.next_transit(sun,start=day))).total_seconds()
            
            pic_filename = (re.sub(regex,subst,str(closest_pic)))
            pic_path = str(root_path + "/" + camera + "/" + day + "/" +pic_filename)
            print("Pic path is: " + pic_path +  " difference is: " + str(time_diff))
            if(time_diff < 60):
                shutil.copy2(pic_path,noon_cam_path + pic_filename)

