import logging
import sys
import os
import readconf_func

confvar=readconf_func.readconf();

LOG_FILE = confvar.get('LOG_FILE')
if LOG_FILE == '' :
   print 'No LOG_FILE key found in conf file ! Exiting...'
   sys.exit()


logger = logging.getLogger('cft') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger1 = logging.getLogger('globus_url_copy') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger1.addHandler(hdlr)
logger1.setLevel(logging.DEBUG)

logger2 = logging.getLogger('cft3') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger2.addHandler(hdlr)
logger2.setLevel(logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
#console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
#formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
# tell the handler to use this format
#console.setFormatter(formatter)
# add the handler to the root logger
#logging.getLogger('').addHandler(console)
