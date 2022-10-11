# Maintenance window calculator

Calculate next available maintenance windows for DigitalOcean regions.

## Usage

Use [the `venv` module](https://docs.python.org/3/library/venv.html#module-venv) to create a virtual environment in the `venv` directory:

```shell
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```shell
pip install -r requirements.txt
```

Run the app with Flask (in development) or Gunicorn (in production):

```shell
FLASK_ENV=development flask run
gunicorn app:app
```
