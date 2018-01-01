import sys
from exodus_core.helper.connector import ExodusConnector
import config as c

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:')
        print('python exodus_download.py <report uri> <destination folder>')

    uri = sys.argv[1]
    destination = sys.argv[2]
    ec = ExodusConnector(c.CONFIG['host'], uri)
    ec.login(c.CONFIG['username'], c.CONFIG['password'])
    ec.get_report_info()
    print('Downloading the APK ...')
    apk_path = ec.download_apk(destination)
    print('Your APK have been successfully downloaded: %s ' % apk_path)