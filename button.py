import os

import subprocess

import RPi.GPIO as GPIO

import time

import sys
import signal



def signal_term_handler(signal, frame):
    print 'got SIGTERM'
    GPIO.cleanup()
    path = "*.h264"
    os.chmod(path, stat.S_IWOTH | stat.S_IROTH)
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)

from subprocess import check_output

def get_pid(name):
    return check_output(["pidof",name])

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)

dateiname = ""

try:
    while True:

        input_state = GPIO.input(18)

        cameraRunning = os.path.isfile("running.flg");

        if(cameraRunning == False):

	    GPIO.output(25,0)

        if(cameraRunning == True):
	    GPIO.output(25,1)


        if input_state == False:

            print('Button Pressed')
  	    timestr = time.strftime("%Y%m%d-%H%M%S")
		


	    wholePathUsed = "/home/pi/twitterbot/video/"+dateiname+".h264"


	    cameraRunning = os.path.isfile("running.flg");

	    if(cameraRunning == False):

		GPIO.output(25,1)

		open('running.flg','a').close()



	        dateiname = "infrarot_schlafaufnahme_" + timestr	


                command = "nohup raspivid -t 0 --width 640 --height 480 --bitrate 42000 --framerate 22 -o /home/pi/twitterbot/video/"+dateiname+".h264&"

		print("Camera is not running, starting camera...")

		print("Filename is: "+ wholePathUsed)

		spawn = True

		if(spawn == True):

			subprocess.Popen([command],
        		         stdout=open('out.txt', 'w'),
                		 stderr=open('logfile.log', 'a'),
	                	 preexec_fn=os.setpgrp,
				 shell=True
				 )
	        time.sleep(0.2)

	    if(cameraRunning == True):

		GPIO.output(25,0)
		
		os.remove("running.flg")

		pid = subprocess.check_output("sudo pgrep rasp",shell=True);
		

		print("Camera is running, shuting down cameraa process id: "+pid);

                #cameraProcessID = get_pid("rasp");

                #print("Camera Prozess ID : "+cameraProcessID)

		subprocess.Popen(["sudo pkill rasp"],shell=True)

		# setting the camera files to be readable by everyone
		# this is usefull when using an ftp programm and want to be able
		# to delete the file afterwards

		wholePath = "/home/pi/twitterbot/video/"+dateiname+".h264"

		subprocess.call(['chmod', '777', wholePath])

		time.sleep(0.2)

except KeyboardInterrupt:

	GPIO.cleanup()
