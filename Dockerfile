FROM python:3.7.4-slim-stretch

RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

ENV APP_PORT 9090

EXPOSE ${APP_PORT}

ENTRYPOINT [ "python", "server.py" ]

# CMD ["python", "server.py"]