FROM python:3.10.6-slim

COPY chess_winner /chess_winner
COPY api /api
COPY model /model
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY Makefile /Makefile

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

CMD uvicorn api.fast:app --reload --host 0.0.0.0 --port $PORT
