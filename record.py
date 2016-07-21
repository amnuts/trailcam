#!/usr/bin/env python

import json
import os
import picamera
import time
import RPi.GPIO as GPIO
from datetime import datetime


def get_filename():
    global config
    return config['save_path'] % datetime.now().strftime('%Y%m%d-%H%M%S')


def pir_triggered():
    global config, lastSeen, recording, camera
    lastSeen = datetime.now()
    if not recording:
        print "Starting up the recording"
        recording = True
        path = get_filename()
        camera.start_recording(path)
        camera.wait_recording(config['record_seconds'])


with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

GPIO.setmode(GPIO.BCM)
GPIO.setup(config['pir_pin'], GPIO.IN)

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.led = False

recording = False
lastSeen = datetime.now()

GPIO.add_event_detect(config['pir_pin'], GPIO.RISING, callback=pir_triggered)

print "Starting in 10 seconds"
time.sleep(10)
print "Go!"

try:
    while True:
        if recording:
            print "Currently recording"
            delta = datetime.now() - lastSeen
            if delta.seconds > config['record_seconds']:
                print "Stopping the video"
                camera.stop_recording()
                recording = False
            else:
                print "Still movement, waiting some more"
                camera.wait_recording(config['record_seconds'])
        else:
            print "Not currently recording"
        time.sleep(1)

except KeyboardInterrupt:
    if recording:
        camera.stop_recording()
    GPIO.cleanup()

if recording:
    camera.stop_recording()
GPIO.cleanup()
