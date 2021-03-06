# Note

1. Finished all required and bonus functions.

2. Addtional python pageage - pymongo is used to store the search results into MongoDB (package dependency has been added into requirements.txt)

3. To test pagination, try to get http://127.0.0.1:8000/users/tj?per_page=10&page=2 while the flask server is running.(you can change number for per_page and page as you want)

4. To test error handling for getting user's gists, you can try to get the gists from a user who does not exists, for examplp, tring to get  http://127.0.0.1:8000/users/ustdionysusfdsafdas

5. To test search api, try the command in terminal: 

   curl -H "Content-Type: application/json" -X POST -d '{"username": "justdionysus", "pattern": "TerbiumLabsChllenge_[0-9]+"}'  http://127.0.0.1:8000/api/v1/search

6. To test error handling for the searching api, you can try the following requests:

   curl -H "Content-Type: application/json" -X POST -d '{"username": "justdionysus"}'  http://127.0.0.1:8000/api/v1/search

   curl -H "Content-Type: application/json" -X POST -d '{"pattern": "TerbiumLabsChllenge_[0-9]+"}'  http://127.0.0.1:8000/api/v1/search

   curl -H "Content-Type: application/json" -X POST -d '{"username": "justdionysusdasffdsa", "pattern": "TerbiumLabsChllenge_[0-9]+"}'  http://127.0.0.1:8000/api/v1/search

7. To test storing search results into the database, make sure you have MongoDB installed and the service is running.Then uncomment the codes for storing in gistapi.py (check the codes in gistapi.py for more details)

# gistapi
Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists. The gistapi code in this repository has 
been left incomplete for you to finish.

## Contents
This project contains a [tox](https://testrun.org/tox/latest/) definition for testing against both Python 2.7 and Python 3.4.
There is a `requirements.txt` file for installing the required Python modules via pip.  There is a `Dockerfile` and `docker-compose.yml` file 
if you'd like to run the project as a docker container.  The `tests/` directory contains two very simple tests to get started.  The `gistapi/`
directory contains the code you'll want to modify to implement the desired features.


## Environment
The project assumes Python 2.7 is installed and libffi and libssl development libraries are installed.  If you plan to use tox to run the tests, 
you should pip install tox also.  If you plan to use docker and docker-compose those will have to be installed.

## Development
The code will be checked while running in a [Docker](https://www.docker.com/) container but there is no requirement to develop/test inside 
docker.  The simplest way is to use a virtualenv for development:

```bash
    ~/Projects/coding_challenge% virtualenv ./env
    New python executable in /home/dion/Projects/coding_challenge/env/bin/python
    Installing setuptools, pip, wheel...done.
    ~/Projects/coding_challenge% source env/bin/activate
    (env) ~/Projects/coding_challenge% pip install -r requirements.txt
    Collecting Flask==0.10.1 (from -r requirements.txt (line 7))
    ...
    Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 gunicorn-19.4.5 itsdangerous-0.24 requests-2.9.1 six-1.10.0
    (env) ~/Projects/coding_challenge% python -m gistapi.gistapi
     * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger pin code: 111-111-111
	
    # In another terminal:
    ~/Projects/coding_challenge% curl -H "Content-Type: application/json" \
           -X POST \
           -d '{"username": "justdionysus", "pattern": "LOL[ab]*"}' \
           http://127.0.0.1:8000/api/v1/search
    {
      "matches": [],
      "pattern": "LOL[ab]*",
      "status": "success",
      "username": "justdionysus"
    }

    # When done, Ctrl-C in the server window
    # When done working on the code, deactivate the virtualenv:
    (env) ~/Projects/coding_challenge% deactivate
    ~/Projects/coding_challenge%
```

Testing your code can be done via tox.  No virtualenv is necessary; tox takes care of setting up a test environment with Python 2.7.  Running 
the test is as simple as:

```bash
    ~/Projects/coding_challenge% sudo pip install tox
    ...
    ~/Projects/coding_challenge% tox
    GLOB sdist-make: /home/dion/Projects/coding_challenge/setup.py
    py27 inst-nodeps: /home/dion/Projects/coding_challenge/.tox/dist/gistapi-0.1.0.zip    
    ...
    _______________________________________________________________________ summary ________________________________________________________________________
      py27: commands succeeded
      congratulations :)
    ~/Projects/coding_challenge%
```

You can check for PEP8 compliance and run a few other static analysis checks via a different tox target:

```bash
    ~Projects/coding_challenge% tox -e flake8
    GLOB sdist-make: /home/dion/Projects/coding_challenge/setup.py
    flake8 inst-nodeps: /home/dion/Projects/coding_challenge/.tox/dist/gistapi-0.1.0.zip
    ...
    _______________________________________________________________________ summary ________________________________________________________________________
      flake8: commands succeeded
      congratulations :)
    ~/Projects/coding_challenge%
```
