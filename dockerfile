FROM python:3.10

LABEL Farrar142 "gksdjf1690@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
COPY . .

RUN pip3 install -r requirements.txt
RUN python3 manage.py test
ENTRYPOINT python3 manage.py makemigrations && python3 manage.py migrate