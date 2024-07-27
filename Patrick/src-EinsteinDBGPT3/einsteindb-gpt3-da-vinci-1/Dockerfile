FROM ubuntu:16.04
MAINTAINER einstAI "whtcorpsarpanet@gmail.com"

# Install dependencies
RUN apt-get -y update
RUN apt-get -y install python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]

# Path: Patrick/src-EinsteinDBGPT3/DiabloGPT-da-vinci-1/app.py
ADD DiabloGPT.tar.gz /home/
RUN pwd
WORKDIR /home/DiabloGPT

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Patrick
RUN python setup.py install

# Upgrade pip
RUN pip install --upgrade pip

# Install project dependencies
RUN pip install -r requirements.txt
