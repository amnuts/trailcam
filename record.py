#!/usr/bin/env python

import json
import os
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
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

camera = PiCamera()
camera.resolution = (1280, 720)
camera.led = False

recording = False
lastSeen = datetime.now()

GPIO.add_event_detect(config['pir_pin'], GPIO.RISING, callback=pir_triggered)

if config['delay_start_seconds']:
    if config['debug_output']:
        print "Starting in %d seconds" % config['delay_start_seconds']
    sleep(config['delay_start_seconds'])
    if config['debug_output']:
        print "Go!"

try:
    while True:
        if recording:
            if config['debug_output']:
                print "Currently recording"
            delta = datetime.now() - lastSeen
            if delta.seconds > config['record_seconds']:
                if config['debug_output']:
                    print "Stopping the video"
                camera.stop_recording()
                recording = False
            else:
                if config['debug_output']:
                    print "Still movement, waiting some more"
                camera.wait_recording(config['record_seconds'])
        else:
            if config['debug_output']:
                print "Not currently recording"
        sleep(config['sleep_seconds'])

except KeyboardInterrupt:
    if recording:
        camera.wait_recording(0)
        camera.stop_recording()
    GPIO.cleanup()

if recording:
    camera.wait_recording(0)
    camera.stop_recording()
GPIO.cleanup()
