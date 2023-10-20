FROM python:3.10.12

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x /booking/docker/*.sh






