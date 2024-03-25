FROM ubuntu:22.04

COPY chess_winner /chess_winner
COPY api /api
COPY model /model
COPY games /games
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY Makefile /Makefile

RUN apt-get update
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

CMD uvicorn api.fast:app --reload --host 0.0.0.0 --port $PORT
