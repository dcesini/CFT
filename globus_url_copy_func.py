#! /usr/bin/python
import os
import logging
import logpredef_cft

logger = logging.getLogger('globus_url_copy')
#globus-url-copy 1.tar.gz gsiftp://darkstorm.cnaf.infn.it:2811//storage/gridit/1.tar.gz

def globus_url_copy(confvar, file_in, file_out):
   cmd = "globus-url-copy -vb " + confvar.get("GFTP_LOCAL_PATH") + '/' + file_in + " gsiftp://" + confvar.get("GFTP_SERVER") + ':' + confvar.get("GFTP_PORT") + '/' + confvar.get("GFTP_REMOTE_PATH") + '/' + file_out     +    " >> " + confvar.get("GFTP_LOG") + " 2>&1"

   logger.info("CMD = " + cmd)

   status = os.system(cmd)

   if status == 0:
      logger.info("File copied!")
   else:
      logger.error("Cannot copy " + confvar.get("GFTP_LOCAL_PATH") + '/' + file_in + " to " + "gsiftp://" + confvar.get("GFTP_SERVER") + ':' + confvar.get("GFTP_PORT") + confvar.get("GFTP_REMOTE_PATH") + '/' + file_out)
      logger.error("Globus-url-copy returned : " + str(status) )

   return status

