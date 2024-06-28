TGramBot
===

A Telegram Bot Control Center to send messages to list of channels

## Contribution Guidelines

To contribute to this project, please follow the guidelines below:

- Fork the repository and create your branch from `main`.
- Make sure your code adheres to the coding standards and passes all the automated tests.
- Submit a pull request (PR) with your changes.
- Your PR will be reviewed by the maintainers, and feedback will be provided if necessary.
- Once approved, your PR will be merged into the main branch.

Please note that all contributions must pass automated tests and adhere to the coding standards set for this project.

## Pre-requisites

- Python 3
- API Credentials (`api_key` and `api_hash`): https://my.telegram.org

---

## Installation

- `python3 -m pip install -r requirements.txt`

---

## Running the Desktop App

- `python3 telegram/gui/telegram_gui.py`
- OR
- `python3 main.py`

---

## Running the API Server

### Run with Python 3

- `python3 telegram/api/server.py`

### Run with Docker

- `docker build -t tgram-bot .`
- `docker run -p 9090:9090 tgram-bot`

---

## Flow

- Obtain `api_key` and `api_hash` from https://my.telegram.org
- Use `/sessions/initiate` API Call to Initiate the session
  - This API Accepts: `api_key, api_hash, session`, and `phone` as query parameters
  - Once this is successful, telegram server will send a "code" on the "phone" no. specified
- Use `/sessions/start` API Call to Start the session
  - This API Accepts: `phone` and `code` as query parameter
  - If this is successful, we can start using APIs to send messages
- Use `/channels/join` API to join list of channels
  - This API Accepts: `channels` parameters as comma separated list in query parameter
- Use `/messages/send` API to send messages to the list of channels
  - This API is flexible, if channels are not joined, then it will try to join the channel first
  - This API Accepts: `channels` and `message` parameters in query parameter

---

## API Docs

- `/api/docs` URL contains the API Docs

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
- [x] Auto Reload of App when any code changes (`auto_reload=True` option)
- [x] Dockerize the app
- [x] Kubernetes Deployment of the app (`/deploy` folder)
- [x] OpenAPI Specs
- [ ] Authentication Support - `https://sanic-jwt.readthedocs.io/en/latest/pages/simpleusage.html`
- [ ] Feeds API with Socket Streaming Support 
- [x] Have a better folder and filer structure
- [ ] CLI - `python main.py`
    - `https://github.com/google/python-fire`
- [x] API - Done using Sanic
- [ ] Web UI
- [x] GUI 
  - [ ] Gooey - `https://github.com/chriskiehl/Gooey`
  - [x] Using PyQt and QtCreator `https://wiki.python.org/moin/PyQt/Tutorials`
- [ ] TUI - Using ncurses
- [x] Package app into a executable
- [ ] Serve with nginx - `https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04`
- [ ] Integrate with Error Tracking Services like Rollbar, Sentry
  - `https://github.com/serathius/sanic-sentry`
- [ ] Make pip module

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

https://t.me/PixelExperience

https://t.me/xXx_OP6_Lounge



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


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


loop.create_task(client.send_message('TelethonOfftopic', 'Hey guys!'))

pending = asyncio.Task.all_tasks()



  loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in range(6)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))



import threading

def fire_and_forget(f):
    def wrapped():
        threading.Thread(target=f).start()

    return wrapped

@fire_and_forget
def foo():
    time.sleep(1)
    print("foo() completed")



```

---

### GUI

```



    pip3 install PyQt5==5.11.3

    # self.setWindowIcon(QtGui.QIcon("icon.png"))
    # self.resize(500,650)
    # self.setMinimumSize(500,650)
    # self.center()
    
    # --- Menu --- #
    open = QAction("Exit", self)
    save = QAction("Save", self)
    build = QAction("Build", self)
    exit = QAction("Quit", self)
    
    menu_bar = QMenuBar()
    file1 = menu_bar.addMenu("&File")
    help = menu_bar.addMenu("&Help")
    
    file1.addAction(open)
    file1.addAction(save)
    file1.addAction(build)



    self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
    self.tab_widget.setTabShape(QTabWidget.TabShape.Triangular)




    # data = loop.run_until_complete(bot.initiate(self.loop))
    # done, pending = loop.run_until_complete(asyncio.wait(await bot.initiate(self.loop)))
    # for future in done:
    #     data = future.result()
    #     print(data)


    # async with data_future as data:

     # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)



    pyuic4 -x test.ui -o test.py 

    pyuic5 mydesign.ui -o mydesign.py


    pip install pyinstaller

    pyinstaller --onefile --windowed app.py
    
    pyinstaller --onefile --windowed telegram/gui/telegram_gui.py

    # --onedir for DEBUG

    pyinstaller app.py

        def get_ui_path(self, ui_file):
      if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        ui_path = f'{bundle_dir}/{ui_file}'
      else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = f'{bundle_dir}/ui/{ui_file}'
      print('bundle_dir', bundle_dir)
      print('ui_path', ui_path)
      return ui_path


C:/Users/<USER>/AppData/Local/<APPNAME>

~/Library/Application Support/<APPNAME>

```
