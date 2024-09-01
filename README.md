# Polls web-application for KU community.

![Flake8 Status](./flake8-badge.svg)

KU-polls is a free minimal and easy to use web-application for conduct a poll or a surveys base on [Django Tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/). You're able to create and conduct a new poll with a start and expire date for each poll. ku-polls also collect a response data and summarize it for you.

Powered by Python with Django web framework

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation
Install requirement
```pip install -r requirements.txt```

## Run the web-application
Change directories to work directories
```bash
cd ku-polls
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
python manage.py loaddata data/polls-v2.json
```

Configs

Get django secret key by run
```
python get_secret_key.py
```

paste it in [sample.env](./sample.env)

rename sample.env to .env
```
mv sample.env .env
```

Initialize server
```bash
python manage.py runserver
```

## Project documentation

### Project Wiki
All project documents are in the  [Wiki page](../../wiki/Home)
* [Vision and scope](../../wiki/Vision-and-Scope)
* [Requirement](../../wiki/Requirement)
* [Project Plan](../../wiki/Vision-and-Scope)

### Iteration plan
* [Iteration 1](../../wiki/iteration1-plan)
* [Iteration 2](../../wiki/iteration2-plan)
