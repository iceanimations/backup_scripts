import os
import subprocess
import logging
import zipfile
import tempfile

tempdir = os.environ['TEMP']

from backup_config import (logdir, logfilename, backupdir, pg_dumpall,
        backupname, getNowString, zipped)


logfile = os.path.join(logdir, logfilename)
logging.basicConfig(filename=logfile, level=logging.DEBUG)


def makeZipped(inpath, outpath):
    zfile = zipfile.ZipFile(outpath, mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    zfile.write(inpath, os.path.basename(inpath))
    zfile.close()
    return True

def create_backup(zipped=True):
    nowString = getNowString()
    dump_base = '_'.join([backupname, nowString + '.sql'])
    dump_path = os.path.join(backupdir, dump_base)

    if zipped:
        dump_path = os.path.join(tempdir, dump_base)
        if os.path.exists(dump_path):
            os.unlink(dump_base)
        ziploc = os.path.join(backupdir, dump_base + '.zip')

    command = [pg_dumpall]
    command.append('-U postgres'.split())
    try:
        logging.info(nowString)
        logging.info('Creating Database Dump ...')
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        logging.info(stderr)
        with open(dump_path, 'w+') as f:
            f.write(stdout)
        logging.info('Dump Done!')
    except subprocess.CalledProcessError as e:
        logging.error(str(e))

    try:
        if zipped:
            logging.info('Making Zip File ...')
            makeZipped(dump_path, ziploc)
            logging.info('Zip Done')
            logging.info('Deleting dump file')
            os.unlink(dump_path)
    except IOError:
        logging.error(str(e))

if __name__ == "__main__":
    create_backup(zipped)

