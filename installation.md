# Installation & Setup guide

Clone repositories
```
git clone https://github.com/opxz7148/ku-polls.git
```

Change current directories
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
```
pip install -r requirements.txt
```

Migrate database
```
python manage.py makemigrations
```
```
python manage.py migrate
```

Load data into database
```
python manage.py loaddata data/polls-v4.json
```
```
python manage.py loaddata data/users.json
```
```
python manage.py loaddata data/votes-v4.json
```

Configs

rename sample.env to .env
```
mv sample.env .env
```