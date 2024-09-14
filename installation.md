# Installation & Setup guide

Change directories to work directories
```bash
cd ku-polls
```

Create virtual enviroment
```
python -m venv .venv
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
python manage.py loaddata data/votes.json
```

Configs

rename sample.env to .env
```
mv sample.env .env
```