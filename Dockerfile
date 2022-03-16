FROM python:3.9-slim-bullseye

RUN apt-get update \
 && apt-get install -y --no-install-recommends dexdump=10.0* \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY exodus_analyze.py .

ENTRYPOINT ["/exodus_analyze.py"]
CMD ["app.apk"]
