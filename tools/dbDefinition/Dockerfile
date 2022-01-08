FROM ubuntu

RUN apt update
RUN apt upgrade -y
RUN apt install graphviz -y

RUN apt-get install python3 -y

RUN apt install python3-pip -y

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY requirements2.txt .
RUN python3 -m pip install -r requirements2.txt

RUN python3 --version

WORKDIR /app
COPY . /app

CMD ["python3", "/app/app.py"]