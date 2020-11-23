import os
import time

if __name__ == '__main__':
    now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    pic_name = 'test1_' + now_time + '.jpg'
    take_pic_command_string = "fswebcam -d /dev/video0 --no-banner -F 20 -r 1920*1080 /home/pi/Pictures/{}".format(
        pic_name)
    os.system(take_pic_command_string)
