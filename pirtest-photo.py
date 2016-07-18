import os
import RPi.GPIO as GPIO
import time
import json
from datetime import datetime  

GPIO.setmode(GPIO.BCM)
with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

GPIO.setup(config['pir'], GPIO.IN)

try:
	print "PIR Module Test (CTRL+C to exit)"
	time.sleep(2)
	print "Ready"
	while True:
		if GPIO.input(config['pir']):
			print "%s %s" % (int(round(time.time() * 1000)), ": motion detected")
			i = datetime.now() 
			now = i.strftime('%Y%m%d-%H%M%S')
			cmd = config['photo'] % now
			os.system(cmd)
		time.sleep(0.5)

except KeyboardInterrupt:
	print "Quit"
	GPIO.cleanup()

