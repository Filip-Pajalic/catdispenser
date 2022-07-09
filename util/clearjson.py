import json
import logging
from datetime import date

logging.basicConfig(filename="/home/pi/log/dispenser.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


with open('/home/pi/config/config.json') as json_file:
    data = json.load(json_file)

today = date.today()
d1 = today.strftime("%y%m%d")

data['date calculated'] = d1

logging.info("Date: " + str(data['date calculated']))

logging.info("--------------------------------------------------------")
logging.info("date: " + str(data['date calculated']))    
logging.info("feed1 amountgiven: " + str(data['feed1']['amountgiven']))
logging.info("feed1 time: " + str(data['feed1']['time']))
logging.info("feed1 deviation: " + str(data['feed1']['deviation']))
logging.info("feed1 deviation: " + str(data['feed1']['skip']))
logging.info("feed1 deviation: " + str(data['feed1']['error']))
logging.info("feed1 deviation: " + str(data['feed1']['error-reason']))

logging.info("--------------------------------------------------------")
logging.info("feed2 amountgiven: " + str(data['feed2']['amountgiven']))
logging.info("feed2 time: " + str(data['feed2']['time']))
logging.info("feed2 deviation: " + str(data['feed2']['deviation']))
logging.info("feed2 deviation: " + str(data['feed2']['skip']))
logging.info("feed2 deviation: " + str(data['feed2']['error']))
logging.info("feed2 deviation: " + str(data['feed2']['error-reason']))

logging.info("--------------------------------------------------------")
logging.info("feed3 amountgiven: " + str(data['feed3']['amountgiven']))
logging.info("feed3 time:" + str(data['feed3']['time']))
logging.info("feed3 deviation: " + str(data['feed3']['deviation']))
logging.info("feed3 deviation: " + str(data['feed3']['skip']))
logging.info("feed3 deviation: " + str(data['feed3']['error']))
logging.info("feed3 deviation: " + str(data['feed3']['error-reason']))

logging.info("--------------------------------------------------------")
logging.info("other amountgiven: " + str(data['other']['amountgiven']))
logging.info("other time:" + str(data['other']['time']))
logging.info("other deviation: " + str(data['other']['deviation']))
logging.info("other deviation: " + str(data['other']['error']))
logging.info("other deviation: " + str(data['other']['error-reason']))

data['feed1']['amountgiven'] = 0
data['feed1']['time'] = 0
data['feed1']['deviation'] = 0
data['feed1']['skip'] = "false"
data['feed1']['error'] = "none"
data['feed1']['error-reason'] = ""

data['feed2']['amountgiven'] = 0
data['feed2']['time'] = 0
data['feed2']['deviation'] = 0
data['feed2']['skip'] = "false"
data['feed2']['error'] = "none"
data['feed2']['error-reason'] = ""

data['feed3']['amountgiven'] = 0
data['feed3']['time'] = 0
data['feed3']['deviation'] = 0
data['feed3']['skip'] = "false"
data['feed3']['error'] = "none"
data['feed3']['error-reason'] = ""

data['other']['status'] = "false"
data['other']['amountgiven'] = 0
data['other']['time'] = 0
data['other']['deviation'] = 0
data['other']['error'] = "none"
data['other']['error-reason'] = ""

data['total']['deviation'] = 0
data['total']['amountgiven'] = 0

with open('/home/pi/config/config.json', 'w') as f:
    json.dump(data, f , indent=4)