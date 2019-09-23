TGramBot
===

A Telegram Bot Control Center to send messages to list of channels


## Pre-requisites

- Python 3
- API Credentials (API_KEY and API_HASH): https://my.telegram.org

---

## Flow

- Obtain `api_key` and `api_hash` from https://my.telegram.org
- Use `/sessions/initiate` API Call to Initiate the session
  - This API Accepts: `api_key, , session, phone` as query parameters
  - Once this is successful, telegram server will send a "code" on the "phone" no. specified
- Use `/sessions/start` API Call to Start the session
  - This API Accepts: `code` as query parameter
  - If this is successful, we can start using APIs to send messages
- Use `/channels/join` API to join list of channels
  - This API Accepts: `channels` parameters as comma separated list in query parameter
- Use `/messages/send` API to send messages to the list of channels
  - This API Accepts: `channels` and `message` parameters in query parameter

---

## API Docs

- `/api/docs` URL contains the API Docs

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
- pythonanywhere.com
- codenvy - Python version issue

Ref: https://blog.codeship.com/the-shortlist-of-docker-hosting/

---

## To Do
- [x] Functionality using Command Line
- [x] Functionality using HTTP APIs (Sanic)
  - [ ] Change some APIs to `POST, DELETE` HTTP Methods
- [x] Auto Reload of App when any code changes (`--reload` option)
- [x] Dockerize the app
- [x] Kubernetes Deployment of the app (`/deploy` folder)
- [x] OpenAPI Specs
- [ ] Authentication Support - `https://sanic-jwt.readthedocs.io/en/latest/pages/simpleusage.html`
- [ ] Feeds API with Socker Streaming Support 
- [ ] Have a better folder and filer structure
- [ ] UI
  - [ ] CLI - `python main.py`
      - `https://github.com/google/python-fire`
  - [ ] Web UI
  - [ ] GUI - `https://github.com/chriskiehl/Gooey`
  - [ ] TUI - Using ncurses
- [ ] Serve with nginx - `https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04`
- [ ] Integrate with Error Tracking Services like Rollbar, Sentry
  - https://github.com/serathius/sanic-sentry

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

```