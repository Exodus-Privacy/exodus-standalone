FROM python:3.7-slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends dexdump=8.1.0+r23-3 \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "exodus_analyze.py", "app.apk"]
