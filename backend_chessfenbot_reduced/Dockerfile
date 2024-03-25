FROM python:3.8.12-slim

COPY chessfenbot_reduced chessfenbot_reduced
COPY saved_models saved_models
COPY board.jpeg board.jpeg
COPY LICENSE LICENSE
COPY requirements.txt requirements.txt
COPY setup.py setup.py

RUN pip install -e .

# when running locally
#CMD uvicorn chessfenbot_reduced.api_file:app --host 0.0.0.0

# when deployed
CMD uvicorn chessfenbot_reduced.api_file:app --host 0.0.0.0 --port $PORT
