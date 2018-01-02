# εxodus standalone
εxodus CLI client for local APK static analysis.

## Installation 
Clone this repository:
```
git clone https://github.com/Exodus-Privacy/exodus-standalone.git
cd exodus-standalone
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
```
python exodus_analyze.py my_apk.apk
```
be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

## Example of output
```
loading the apk
loading trackers signatures from Exodus
decoding the apk
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

## Pitfalls
This tool uses `dexdump` and only provides `GNU/Linux x86_64` version of it.

# Download an APK from εxodus instance
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
