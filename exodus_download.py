import config
import sys

from exodus_core.helper.connector import ExodusConnector


def main():
    if len(sys.argv) != 3:
        print('Usage:')
        print('python exodus_download.py <report id> <destination folder>')
        sys.exit(1)

    uri = '/api/report/{}/'.format(sys.argv[1])
    destination = sys.argv[2]

    try:
        ec = ExodusConnector(config.CONFIG['host'], uri)
        ec.login(config.CONFIG['username'], config.CONFIG['password'])
        print('Successfully logged in')
        ec.get_report_info()
        print('Downloading the APK ...')
        apk_path = ec.download_apk(destination)
        print('APK successfully downloaded: {}'.format(apk_path))
    except Exception as e:
        print('ERROR: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
