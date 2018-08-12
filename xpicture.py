#!/usr/bin/env python
#coding:utf-8
import picamera
from picamera import PiCamera
import time
import os
"""set camera"""

class xpic():
    def __init__(self,picpath,resolution="640x320",framerate = 15):
        self.cached_dir = '/tmp/.raspx_cached'
        self.cached_file = '/tmp/.raspx_cached/xpic.cached'
        self.picpath = picpath
        self.pic_init()
        self.camera = PiCamera()
        self.camera.resolution = map(lambda resolution:tuple(map(int,resolution)),[resolution.split(filter(lambda x: not str.isdigit(x), resolution))])[0]
        self.camera.framerate = framerate

    def pic_init(self):
        if not os.path.isdir(self.cached_dir):
            os.mkdir(self.cached_dir)
        if not os.path.isfile(self.cached_file):
            with open(self.cached_file,'w') as cachefile:
                cachefile.write(str(round(time.time(),0))+"D")
                cachefile.close()

    def capture(self,time_of_exposure=2,size = 18):
        if self.status_cache():
            Now = round(time.time(),0)
            self.write_cache(Now)
            data = {'stutas':'unknow','time':Now}
            try:
                self.camera.start_preview()
                time.sleep(time_of_exposure)
                NowTime = time.strftime('%Y-%m-%d %H:%M:%S %a', time.localtime(Now))
                self.camera.annotate_background = picamera.Color(96,96,96)
                self.camera.annotate_text = NowTime
                self.camera.annotate_text_size=size
                self.camera.capture(self.picpath)
                self.camera.stop_preview()
                self.camera.close()
                self.done_cache()
                data.update({'stutas':'ok'})
            except:
                data.update({'stutas': 'error'})
            finally:
                return data
        else:
            return {'status':'used','time':open(self.cached_file,'r').read()}

    def lettering(self,word,R=255,B=255,G=0):
        from PIL import Image
        from PIL import ImageDraw
        image=Image.open(self.picpath)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0),word,(R,B,G))
        ImageDraw.Draw(image)
        image.save(self.picpath)

    def status_cache(self):
        with open(self.cached_file,'r') as f:
            f.seek(12)
            s = f.read(1)
            f.close()
            if s == "D":
                return True
            else:return False

    def write_cache(self,time):
        with open(self.cached_file,'w') as cachefile:
            cachefile.write(str(time))
            cachefile.close()

    def done_cache(self):
        with open(self.cached_file,'a+') as cachefile:
            cachefile.write('D')
            cachefile.close()

if __name__ == '__main__':
    picpath = '/home/pi/Pictures/test.jpg'
    pica = xpic(picpath,"1920x1080")
    status = pica.capture()
    print status



