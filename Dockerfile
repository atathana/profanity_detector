FROM python:3.6.15-buster
COPY api /api
COPY requirements.txt /requirements.txt
COPY profanity_detector /profanity_detector
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.frontend_mvp:app --host 0.0.0.0 --port $PORT
