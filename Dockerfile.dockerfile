# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app


# docker rm /ephemeris_timelapse; docker build --pull --rm -f "Dockerfile.dockerfile" -t ephemeristimelapse:latest "." ; docker run  -v '/mnt/user/security_cams/':'/timelapse/':'rw' --name ephemeris_timelapse -e PYTHONUNBUFFERED=0 -e LOGLEVEL=DEBUG -e LONGITUDE=-105.23 -e LATITUDE=40.0 -e TZ=America/Denver -e INPUT_ROOT="/timelapse/FVSYkiwp2G" ephemeristimelapse:latest 
ENV LOGLEVEL=INFO
ENV LONGITUDE
ENV LATITUDE
ENV TZ
ENV INPUT_ROOT
ENV OUTPUT_ROOT
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "ephemeris_timelapse.py"]