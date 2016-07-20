#!/usr/bin/env python

import os, time, json, picamera
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)
with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

GPIO.setup(config['pir'], GPIO.IN)
camera = picamera.PiCamera()
camera.resolution = (640, 480)

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"
    while True:
        if GPIO.input(config['pir']):
            print "%s %s" % (int(round(time.time() * 1000)), ": motion detected")
            i = datetime.now()
            now = i.strftime('%Y%m%d-%H%M%S')
            path = config['video_path'] % now
            camera.start_recording(path)
            camera.wait_recording(config['min_record_len'])
            camera.stop_recording()

except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
