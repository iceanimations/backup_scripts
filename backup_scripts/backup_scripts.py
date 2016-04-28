import os
import subprocess
import logging
import zipfile
import shutil
import traceback

tempdir = os.environ['TEMP']

from backup_config import (logdir, logfilename, backupdir,
        backupname, getNowString, zipped, scripts_location)


logfile = os.path.join(logdir, logfilename)
logging.basicConfig(filename=logfile, level=logging.DEBUG)

def create_backup(zipped=True):
    nowString = getNowString()
    dump_base = '_'.join([backupname, nowString])
    dump_path = os.path.join(backupdir, dump_base)

    if zipped:
        logging.info('Making Zip File ...')
        try:
            shutil.make_archive(dump_path, 'gztar', scripts_location)
            logging.info('Zip Done')
        except Exception as e:
            logging.error(traceback.format_exc())

    else:
        logging.info('Starting Copy ...')
        try:
            shutil.copytree(scripts_location, dump_path)
            logging.info('Copy Done')
        except Exception as e:
            logging.error(traceback.format_exc())


if __name__ == "__main__":
    create_backup(zipped)

