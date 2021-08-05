# εxodus standalone

[![Build Status](https://github.com/Exodus-Privacy/exodus-standalone/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Exodus-Privacy/exodus-standalone/actions/workflows/main.yml)

εxodus CLI client for local APK static analysis.

## Summary

- [**Using Docker**](#using-docker)
- [**Manual usage**](#manual-usage)
  - [**Installation**](#installation)
  - [**Analyze an APK file**](#analyze-an-apk-file)
  - [**Download an APK from an εxodus instance**](#download-an-apk-from-an-εxodus-instance)
- [**Continuous Integration**](#continuous-integration)

## Using Docker

The easiest way to analyze an APK is to use [our Docker image](https://hub.docker.com/r/exodusprivacy/exodus-standalone).

Simply go to the directory where the APK file is and run:

```bash
docker run -v $(pwd)/<your apk file>:/app.apk --rm -i exodusprivacy/exodus-standalone
```

## Manual usage

### Installation

Clone this repository:

```bash
git clone https://github.com/Exodus-Privacy/exodus-standalone.git
cd exodus-standalone
```

Install `dexdump`:

```bash
sudo apt-get install dexdump
```

Create Python `virtualenv`:

```bash
sudo apt-get install virtualenv
virtualenv venv -p python3
source venv/bin/activate
```

Download and install dependencies:

```bash
pip install -r requirements.txt
```

### Analyze an APK file

#### Usage

```bash
$ python exodus_analyze.py -h
Usage: exodus_analyze.py [options] apk_file

Options:
  -h, --help            show this help message and exit
  -t, --text            print textual report (default)
  -j, --json            print JSON report
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        store JSON report in file (requires -j option)
```

#### Text output

```bash
python exodus_analyze.py my_apk.apk
```

be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

*Example:*

```bash
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

#### JSON output

```bash
python exodus_analyze.py -j [-o report.json] my_apk.apk
```

be sure to activate the Python `virtualenv` before running `exodus_analyze.py`.

*Example:*

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

#### Pitfalls

This tool uses `dexdump` and only provides `GNU/Linux x86_64` version of it.

### Download an APK from an εxodus instance

Create `config.py` file in the project directory specifying:

```bash
CONFIG = {
    'username': 'alice',
    'password': 'bob',
    'host': 'http://localhost:8000'
}
```

Run

```bash
python exodus_download.py 15 /tmp/
```

be sure to activate the Python `virtualenv` before running `exodus_download.py`.

#### Example of output

```bash
python exodus_download.py 15 /tmp/
Successfully logged in
Downloading the APK ...
APK successfully downloaded: /tmp/fr.meteo.apk
```

## Continuous Integration

You can use εxodus-standalone in your CI pipelines.

Below are listed some examples of how to integrate it.

:warning: Please note that the task will fail if it finds **any tracker**.

### GitLab CI/CD

```yml
exodus_scan:
  stage: audit
  image:
    name: exodusprivacy/exodus-standalone:latest
    entrypoint: [""]
  script:
    - python /exodus_analyze.py [YOUR_APK_PATH]
```
