FROM alpine
WORKDIR /opt/migrator
ADD . /opt/migrator

RUN apk --update add curl docker python3 py3-pip

RUN pip install -r requirements.txt

CMD python3 /opt/migrator/app.py
