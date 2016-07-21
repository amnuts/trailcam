import RPi.GPIO as GPIO
import time
import json

GPIO.setmode(GPIO.BCM)
with open('config.json', 'r') as f:
    config = json.load(f)

GPIO.setup(config['pir'], GPIO.IN)

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"
    while True:
        if GPIO.input(config['pir']):
            print "%s %s" % (int(round(time.time() * 1000)), ": motion detected")

except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
