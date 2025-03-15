FROM python:3.10-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y tini

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["bash", "-c", "uvicorn api:app --host 0.0.0.0 --port 8001 --reload & python consumer.py"]