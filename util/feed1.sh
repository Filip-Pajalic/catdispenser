kill $(ps aux | grep '[p]ython /home/pi/cronjob/2.py 1' | awk '{print $2}')