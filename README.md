# εxodus standalone
εxodus CLI client for local APK static analysis.

## Installation 
Clone this repository:
```
git clone https://github.com/Exodus-Privacy/exodus-standalone.git
cd exodus-standalone
```
Install `dexdump`:
```
sudo apt-get install dexdump
```
Create a `gplaycli` configuration file:
```
nano ~/.config/gplaycli/gplaycli.conf
```
containing
```
[Credentials]
gmail_address=
gmail_password=
#keyring_service=gplaycli
token=True
token_url=https://matlink.fr/token/email/gsfid

[Cache]
token=~/.cache/gplaycli/token

[Locale]
locale=en_US
timezone=CEST
```

Create Python `virtualenv`:
```
virtualenv venv -p python3
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```

# Analyze an APK file

## Usage
```
$ python exodus_analyze.py -h
Usage: exodus_analyze.py [options] apk_file

Options:
  -h, --help            show this help message and exit
  -t, --text            print textual report (default)
  -j, --json            print JSON report
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        store JSON report in file (requires -j option)
```

## Text output
```
python exodus_analyze.py my_apk.apk
```
be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

### Example of text output
```
=== Informations
- APK path: /tmp/tmp1gzosyt4/com.semitan.tan.apk
- APK sum: 8e85737be6911ea817b3b9f6a80290b85befe24ff5f57dc38996874dfde13ba7
- App version: 5.7.0
- App version code: 39
- App name: Tan Network
- App package: com.semitan.tan
- App permissions: 9
    - android.permission.INTERNET
    - android.permission.ACCESS_NETWORK_STATE
    - android.permission.ACCESS_FINE_LOCATION
    - android.permission.WRITE_EXTERNAL_STORAGE
    - android.permission.READ_PHONE_STATE
    - android.permission.VIBRATE
    - com.semitan.tan.permission.C2D_MESSAGE
    - com.google.android.c2dm.permission.RECEIVE
    - android.permission.WAKE_LOCK
- App libraries: 0
=== Found trackers
 - Google Analytics
 - Google Ads
 - Google DoubleClick
```

## JSON output
```
python exodus_analyze.py -j [-o report.json] my_apk.apk
```
be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

### Example of text output
```json
{
  "trackers": [
    {
      "id": 70,
      "name": "Facebook Share"
    },
    [...]
  ],
  "apk": {
    "path": "com.johnson.nett.apk",
    "checksum": "70b6f0d9df432c66351a587df7b65bea160de59e791be420f0e68b2fc435429f"
  },
  "application": {
    "version_code": "15",
    "name": "Nett",
    "permissions": [
      "android.permission.INTERNET",
      "android.permission.ACCESS_NETWORK_STATE",
      "android.permission.WRITE_EXTERNAL_STORAGE",
      "android.permission.READ_PHONE_STATE",
      "android.permission.READ_EXTERNAL_STORAGE",
      "android.permission.WAKE_LOCK",
      "com.google.android.c2dm.permission.RECEIVE",
      "com.johnson.nett.permission.C2D_MESSAGE"
    ],
    "version_name": "1.1.12",
    "libraries": [],
    "handle": "com.johnson.nett"
  }
}
```

## Pitfalls
This tool uses `dexdump` and only provides `GNU/Linux x86_64` version of it.

# Download an APK from an εxodus instance
Create `config.py` file in the project directory specifying:
```
CONFIG = {
    'username': 'alice',
    'password': 'bob',
    'host': 'http://localhost:8000'
}
```
Run
```
python exodus_download.py /api/report/15/ /tmp/
```
be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

## Example of output
```
python exodus_download.py /api/report/15/ /tmp/                                                                                             1 ↵
Downloading the APK ...
Your APK have been successfully downloaded: /tmp/fr.meteo.apk
```
