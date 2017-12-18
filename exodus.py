import json
import re
import sys
import urllib.request
from hashlib import sha256

from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat


class StaticAnalysis:

    def __init__(self, apk_path):
        self.apk = None
        self.decoded = None
        self.apk_path = apk_path
        self.signatures = None
        self.load_apk()

    def load_trackers_signatures(self):
        """
        Load trackers signatures from the official Exodus database.
        :return: a dictionary containing signatures.
        """
        print('loading trackers signatures from Exodus')
        exodus_url = "https://reports.exodus-privacy.eu.org/api/reports"
        with urllib.request.urlopen(exodus_url) as url:
            data = json.loads(url.read().decode())
            self.signatures = data['trackers']

    def load_apk(self):
        """
        Load the APK file.
        """
        print('loading the apk')
        self.apk = APK(self.apk_path)

    def decode_apk(self):
        """
        Decode the APK file.
        """
        print('decoding the apk')
        self.decoded = DalvikVMFormat(self.apk)

    def detect_trackers(self):
        """
        Detect embedded trackers.
        """
        if self.signatures is None:
            self.load_trackers_signatures()
        if self.decoded is None:
            self.decode_apk()
        print('detecting trackers')
        trackers = []
        for v, i in enumerate(self.signatures):
            for clazz in self.decoded.get_classes_names():
                tracker = self.signatures[i]
                sign = tracker['code_signature']
                if len(sign) > 1:
                    m = re.search(tracker['code_signature'], clazz)
                    if m is not None:
                        trackers.append(tracker)
                        break

        return trackers

    def get_version(self):
        """
        Get the application version name
        :return: version name
        """
        return self.apk.get_androidversion_name()

    def get_version_code(self):
        """
        Get the application version code
        :return: version code
        """
        return self.apk.get_androidversion_code()

    def get_permissions(self):
        """
        Get application permissions
        :return: application permissions list
        """
        return self.apk.get_permissions()

    def get_app_name(self):
        """
        Get application name
        :return: application name
        """
        return self.apk.get_app_name()

    def get_package(self):
        """
        Get application package
        :return: application package
        """
        return self.apk.get_package()

    def get_libraries(self):
        """
        Get application libraries
        :return: application libraries list
        """
        return self.apk.get_libraries()

    def get_sha256(self):
        """
        Get the sha256sum of the APK file
        :return: hex sha256sum
        """
        BLOCKSIZE = 65536
        hasher = sha256()
        with open(self.apk_path, 'rb') as apk:
            buf = apk.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = apk.read(BLOCKSIZE)
        return hasher.hexdigest()

    def print_apk_infos(self):
        """
        Print APK informations
        """
        print("=== Informations")
        print('- APK path: %s' % self.apk_path)
        print('- APK sum: %s' % self.get_sha256())
        print('- App version: %s' % self.get_version())
        print('- App version code: %s' % self.get_version_code())
        print('- App name: %s' % self.get_app_name())
        print('- App package: %s' % self.get_package())
        print('- App permissions: %s' % len(self.get_permissions()))
        for p in self.get_permissions():
            print('    - %s' % p)
        print('- App libraries: %s' % len(self.get_libraries()))
        for l in self.get_libraries():
            print('    - %s' % l)

    def print_embedded_trackers(self):
        """
        Print detected trackers
        """
        trackers = self.detect_trackers()
        print("=== Found trackers")
        for t in trackers:
            print(' - %s' % t['name'])


# Main
analysis = StaticAnalysis(sys.argv[1])
analysis.load_trackers_signatures()
analysis.decode_apk()
analysis.print_apk_infos()
analysis.print_embedded_trackers()