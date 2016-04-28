import os
from backup_config import ( logdir, logfilename, backupdir, maxage, backupname,
        getNowString )
import logging
import glob
import time

logfile = os.path.join(logdir, logfilename)
logging.basicConfig(filename=logfile, level=logging.DEBUG)

now = time.time()

def housekeeping():
    logging.info('Starting Scripts Housekeeping At %s'%getNowString(time.localtime(now)))

    for filename in glob.glob(os.path.join(backupdir, backupname + '*')):

        age = now - os.path.getmtime(filename)

        logging.info('file %s: age=%f maxage=%d %s ...' % (filename, age, maxage,
            '- cleaning' if age > maxage else '- ignoring'))

        if age > maxage:

            logging.info('cleaning %s' % filename)

            try:

                logging.info('deleting file %s' % filename)
                os.unlink(filename)
                logging.info('delete successful')

            except Exception as e:
                logging.error(str(e))


if __name__ == "__main__":
    housekeeping()
