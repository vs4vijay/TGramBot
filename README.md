TGramBot
===

A Telegram Bot Command Center to send messages to list of channels


## Pre-requisite

- Python 3
- Get API Credentials(API_KEY and API_HASH): https://my.telegram.org

---

## Running

### Run with Docker

- `docker build -t tgram-bot .`
- `docker run -p 9999:9090 tgram-bot`

---

### Python ASGI Servers

- Uvicorn 
  -  `uvicorn server:app`
  -  `gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker`
- Hypercorn - `hypercorn server:app`
- Daphne - `daphne server:app`
- Gunicorn
  - `gunicorn server:app --bind 0.0.0.0:9090 --worker-class sanic.worker.GunicornWorker`



---

## Deployment

### Deploy to Heroku

- `heroku login` - Login to Heroku
- `heroku container:login` - Login to Heroku Docker Registery
- `heroku container:push web -a tgram-bot` - Push current local docker image to registery
- `heroku container:release web -a tgram-bot` - Release and Deploy the latest image
- `heroku logs --tail -a tgram-bot-deploy` - To check the logs

### Deployment Options
- OpenShift - Yes
- Repl.it - Yes, but public
- Heroku - Yes
- platform.sh - Nope
- now.sh - Nope
- DigitalOcean - https://marketplace.digitalocean.com/apps/docker
- scalingo.com - No

---

### Development Notes

- API Used: https://docs.telethon.dev/
- Frameworks: Sanic (Based on Event Loop and AsyncIO)
- Docker

```


Test Server: 149.154.167.40:443


@TelethonChat
@TelethonOfftopic

https://t.me/TelethonSnippets

https://telegramchannels.me

https://tlgrm.eu/channels/language




 https://sanic.readthedocs.io/en/latest/sanic/blueprints.html

 if __name__ == ‘__main__’:
 context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
 context.load_cert_chain(“./.ssl/name_of_cert_file.crt”, keyfile=”./.ssl/name_of_key_file.key”)app.go_fast(host=”0.0.0.0", port=8443, ssl=context, workers=os.cpu_count(), debug=True)

from functools import wraps

 def check_request_for_authorization_status(request):
    # Note: Define your check, for instance cookie, session.
    flag = True
    return flag


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


@app.route("/")
@authorized()
async def test(request):
    return json({'status': 'authorized'})


server {

    listen 80;
    server_name app.com;
    charset utf-8;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# handler = logging.StreamHandler()
# logger.addHandler(handler)

---
Auto Reload
Dockerize: `python:3.7.4-slim-stretch`, `python:3.7.4-alpine3.9`
Kubernetes
UI
Structure
HTTP Methods

https://sanic-jwt.readthedocs.io/en/latest/pages/simpleusage.html

https://blog.codeship.com/the-shortlist-of-docker-hosting/

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04


```