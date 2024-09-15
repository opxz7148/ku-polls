# Installation & Setup guide

## Requirement
* Python 3.11 or higher
* git
* pip


## Installation guide

Get the source code.
* clone directories.
    ```bash
    git clone https://github.com/opxz7148/ku-polls.git
    ```

* Download zip file and extract.

Change directories to work directories
```bash
cd ku-polls
```

Create virtual environment

```
python -m venv env
```

Activate virtual environments

* Window 
    ```
    env\Scripts\activate
    ```

* MacOS / Linux 
    ```
    source env/bin/activate
    ```

Install require packages
```bash
pip install -r requirements.txt
```

Migrate database
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Load data into database
```bash
python manage.py loaddata data/polls-v4.json
```
```bash
python manage.py loaddata data/users.json
```
```bash
python manage.py loaddata data/votes-v4.json
```

Configs

Rename sample.env to .env

* Window
    ```bash
    move sample.env .env
    ```

* MacOS / Linux
    ```bash
    mv sample.env .env
    ```