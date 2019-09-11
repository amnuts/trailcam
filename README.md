# trailcam

Record trail cam videos automatically on movement using a Raspberry Pi

# Setup

Once logged into your rpi, clone the repo - it can be wherever you like, but assuming you set this up in `/home/pi`:

```
git clone https://github.com/amnuts/trailcam.git
cd trailcam
```

In the trailcam directory you'll see a `config.json` file that looks like:

```
{
    "pir_pin": 14,
    "save_path": "/home/pi/Videos/trail-%s.h264",
    "delay_start_seconds": 30,
    "sleep_seconds": 2,
    "record_seconds": 10,
    "debug_output": false
}
```

The `pir_bin` define what pin the PIR sensor data output is attached to.  Bear in mind that this is *BCM* numbering, but https://pinout.xyz/ is a great site to see what pins are what.

The `delay_start_seconds` is how long it'll take to start recording from when the script starts - handy if you have it auto-start on the pi booting up.

The `record_seconds` is how long the video should keep recordiong for once it doesn't detect any movement.

`sleep_seconds` is how long it'll sleep before running the recording check loop again.

The `save_path` is where it'll save the file.  The `%s` will be substituted with the current date and time of when the video was recorded.  So if you want the actual date/time then you'll either need an internet connection or a real-time clock module for the rpi.

# Auto-starting

If you wish to have the script run automatically when you boot the rpi, you can edit the `/etc/rc.local` file and add the following line:

```
(su - pi -c "python /home/pi/trailcam/record.py")&
```
