# 235movies.com

## Description

This is my web application which uses a database instead of a memory repo.
## Installation

**Installation via requirements.txt**

```shell
$ cd myfolder
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:mywebsite' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *myfolder* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 
Or run the wsgi.py! Make sure you are in the directory with movies, tests etc.

## Configuration

The *mywebsite/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *COMPSCI-235/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *COMPSCI-235/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'me', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\me\Documents\python-dev\COVID-19\tests\data`

You have to run each test separately.

 