#!/usr/bin/python
import sys,os,time
import readconf_func
import logging
import logpredef_cft
import check_running_func
import globus_url_copy_func
from daemon_class import Daemon


def loadmm(lines):
   d1 = {}
   try:
      idx = lines.index('START OF FILE\n')
   except ValueError:
      return None 
   try:
      idx2 = lines.index('END OF FILE\n')
   except ValueError:
      return None
   for line in lines[idx + 1 : idx2] :
      if line.find('DATE') == -1:
         linesp = line.split()
         nce =  linesp[0].strip().rstrip()
         occ =  linesp[1].strip().rstrip()
         d1[nce] = occ
   return d1



class MyDaemon(Daemon):
        def __init__(self, pidfile, stdin='/dev/null', stdout='/home/cesini/CFT/daemon.log', stderr='/home/cesini/CFT/daemonerr.log'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

        def run(self):
                #INIZIALIZATION
                logger = logging.getLogger('cft')
                TIME_AT_START = time.time()
                confvar=readconf_func.readconf();
                logger.info('#########################################')
                logger.info('## This is the CNAF File Transfer tool ##')
                logger.info('#########################################')
                timenow_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(TIME_AT_START))
                logger.info('cft.py started on ' + timenow_str)
                logger.info('Configuration file read: ' + confvar['CONF_FILE1'])
                logger.info('Configuration file read: ' + confvar['CONF_FILE2'])
                #############################################################
                ### Look for already running wrapper process
                pname = 'cft.py'
                RUNNING = check_running_func.check_running(pname)
                if RUNNING:
                   logger.error('Another cft.py is running. Aborting')
                   sys.exit(1)
                ##############################################################

                #CHECKING MSG PATHS
                if (os.access(confvar.get('INPUT_FILES_PATH'),os.F_OK) == False):
                    logger.error('NOT EXISTING DIRECTORY: ' + confvar.get('INPUT_FILES_PATH') + '. Please check configuration file\n')
                    sys.exit(1)
                if (os.access(confvar.get('PROCESSED_FILES_PATH'),os.F_OK) == False):
                    logger.error('NOT EXISTING DIRECTORY: ' + confvar.get('PROCESSED_FILES_PATH') + '. Please check configuration file\n')
                    sys.exit(1)

                #Starting daemon
                while True:
                      #Checking for new DATA Messages
                      list=os.listdir(confvar.get('INPUT_FILES_PATH'))
                      if len(list) == 0:
                         logger.info("No new file to process")
                      for msg in list:
                          if (os.access(confvar.get('INPUT_FILES_PATH') + '/' + msg,os.F_OK) == True):
                              #ACCESSING INPUT FILE
                              logger.info('Working on file: ' + msg)
                              msghdl = open(confvar.get('INPUT_FILES_PATH') + '/' + msg,'r')
                              lines = msghdl.readlines()
                              for line in lines:
                                  logger.info(line)
                                  linesp = line.split(' ')
                                  if len(linesp) < 2:
                                     logger.error("File " + msg + " wrongly formatted. Please check manually. Exiting!")
                                     sys.exit(1)
                                  else:
                                     file_in = linesp[0].strip().rstrip()
                                     file_out = linesp[1].strip().rstrip()
                                     logger.info("file_in = " + file_in)
                                     logger.info("file_out = " + file_out)
                                     globus_url_copy_func.globus_url_copy(confvar,file_in,file_out)
                              msghdl.close()
                              status = os.system('mv ' + confvar.get('INPUT_FILES_PATH') + '/' + msg + ' ' + confvar.get('PROCESSED_FILES_PATH'))
                              if status != 0:
                                 logger.error('Cannot move processed file to ' + confvar.get('PROCESSED_FILES_PATH') + '. Please check manually. Exiting!\n')
                                 sys.exit(1)

                      logger.info("Waiting for 5 seconds before checking for new files")
                      time.sleep(5)

if __name__ == "__main__":
        daemon = MyDaemon('/home/cesini/CFT/cft.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        print "STARTING CFT DAEMON ..."
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        print "STOPPING CFT DAEMON ..."
                        daemon.stop()
                        print "STOP OK"
                elif 'restart' == sys.argv[1]:
                        print "RESTARTING CFT DAEMON ..."
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)

