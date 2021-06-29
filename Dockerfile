FROM python:3.7.11-slim-stretch

RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PORT 9090

EXPOSE $PORT

ENTRYPOINT [ "python3", "server.py" ]

CMD $PORT