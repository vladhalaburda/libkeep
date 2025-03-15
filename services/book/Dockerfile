FROM python:3.10-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y dumb-init

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["dumb-init", "bash", "-c", "uvicorn api:app --host 0.0.0.0 --port 8002 & python consumer.py"]








# RUN apt-get update && apt-get install -y tini

# ENTRYPOINT ["/usr/bin/tini", "--"]

# CMD ["bash", "-c", "uvicorn api:app --host 0.0.0.0 --port 8002 --reload"]