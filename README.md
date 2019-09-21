


## Pre-requisite

- Python 3
- Get API Credentials: https://my.telegram.org


### Development Notes

```

@TelethonChat
@TelethonOfftopic

https://t.me/TelethonSnippets

https://telegramchannels.me

https://tlgrm.eu/channels/language


ASGI are Daphne, Uvicorn, and Hypercorn.
daphne myapp:app
uvicorn myapp:app
hypercorn myapp:app

gunicorn myapp:app --bind 0.0.0.0:1337 --worker-class sanic.worker.GunicornWorker


 924847283:AAFwZDQMubOUROdWOaaBNDqa5etrDdRB_HM

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


- 
Auto Reload
Dockerize
UI

```