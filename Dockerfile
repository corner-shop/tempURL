FROM python:2.7

EXPOSE 6222
ADD run.py /data/run.py
ADD requirements.txt /data/requirements.txt
WORKDIR /data

RUN pip install -r requirements.txt
CMD python run.py