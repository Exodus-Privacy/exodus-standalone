#!/usr/bin/env python3

import argparse
import config
import os.path
import sys

from exodus_core.helper.connector import ExodusConnector


def download_apk(report_id, destination):
    uri = '/api/report/{}/'.format(report_id)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report_id', type=int, help='the report of the app to download')
    parser.add_argument('destination', help='the destination folder')

    args = parser.parse_args()
    if not os.path.isdir(args.destination):
        print('ERROR: destination argument needs to be a directory')
        parser.print_help()
        sys.exit(1)

    download_apk(args.report_id, args.destination)


if __name__ == '__main__':
    main()
