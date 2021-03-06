import json
import optparse
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


def main():
    parser = optparse.OptionParser('usage: %prog [options] apk_file')
    parser.add_option(
        '-t', '--text',
        dest='text_mode',
        action='store_true',
        default=True,
        help='print textual report (default)'
    )
    parser.add_option(
        '-j', '--json',
        dest='json_mode',
        action='store_true',
        default=False,
        help='print JSON report'
    )
    parser.add_option(
        '-o', '--output',
        dest='output_file',
        default=None,
        help='store JSON report in file (requires -j option)'
    )

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('incorrect number of arguments')
        sys.exit(1)

    apk_file = args[0]

    analysis = AnalysisHelper(apk_file)
    analysis.load_trackers_signatures()
    if options.json_mode:
        report = json.dumps(analysis.create_json_report(), indent=2)
        if options.output_file:
            with open(options.output_file, 'w') as out:
                out.writelines(report)
        else:
            print(report)
    else:
        analysis.print_apk_infos()
        analysis.print_embedded_trackers()

    sys.exit(len(analysis.detect_trackers()))


if __name__ == '__main__':
    main()
