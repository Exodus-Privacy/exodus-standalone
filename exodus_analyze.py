#!/usr/bin/env python3

import argparse
import json
import os.path
import sys

from exodus_core.analysis.static_analysis import StaticAnalysis


class AnalysisHelper(StaticAnalysis):
    def create_json_report(self):
        return {
            'application': {
                'handle': self.get_package(),
                'version_name': self.get_version(),
                'version_code': self.get_version_code(),
                'uaid': self.get_application_universal_id(),
                'name': self.get_app_name(),
                'permissions': self.get_permissions(),
                'libraries': [library for library in self.get_libraries()],
            },
            'apk': {
                'path': self.apk_path,
                'checksum': self.get_sha256(),
            },
            'trackers': [
                {'name': t.name, 'id': t.id} for t in self.detect_trackers()
            ],
        }


def validate_arguments(args):
    if not os.path.isfile(args.apk):
        return 'apk file should exist'

    if args.output_file and not args.json_mode:
        return 'output_file option requires JSON mode'

    return ''


def raise_error(parser, error_msg):
    print('ERROR: {}'.format(error_msg))
    parser.print_help()
    sys.exit(1)


def get_ignore_list(ignore_arg):
    ignored = []

    if ignore_arg:
        try:
            ignored = [int(id) for id in ignore_arg.split(',')]
        except Exception:
            return [], 'incorrect ignore argument'

    return ignored, ''


def analyze_apk(apk, json_mode, output_file, forced_code, ignore_list):
    analysis = AnalysisHelper(apk)
    analysis.load_trackers_signatures()
    if json_mode:
        report = json.dumps(analysis.create_json_report(), indent=2)
        if output_file:
            with open(output_file, 'w') as out:
                out.writelines(report)
        else:
            print(report)
    else:
        analysis.print_apk_infos()
        analysis.print_embedded_trackers()

    trackers_not_ignored = [t for t in analysis.detect_trackers() if t.id not in ignore_list]
    counter = len(trackers_not_ignored)
    if all([counter, forced_code is not None]):
        sys.exit(forced_code)
    sys.exit(counter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('apk', help='the apk file to analyse')
    parser.add_argument(
        '-t', '--text',
        dest='text_mode',
        action='store_true',
        default=True,
        help='print textual report (default)'
    )
    parser.add_argument(
        '-j', '--json',
        dest='json_mode',
        action='store_true',
        default=False,
        help='print JSON report'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default=None,
        help='store JSON report in file (requires -j option)'
    )
    parser.add_argument(
        '-i', '--ignore',
        dest='ignore',
        default=None,
        help='comma-separated ids of trackers to ignore'
    )
    parser.add_argument(
        '-e', '--exit-code',
        metavar='CODE',
        dest='override_code',
        type=int,
        help='use the CODE instead of trackers counter as exit code if trackers was detected'
    )

    args = parser.parse_args()
    args_error = validate_arguments(args)

    if args_error:
        raise_error(parser, args_error)

    ignore_list, ignore_error = get_ignore_list(args.ignore)

    if ignore_error:
        raise_error(parser, ignore_error)

    analyze_apk(args.apk, args.json_mode, args.output_file, args.override_code, ignore_list)


if __name__ == '__main__':
    main()
