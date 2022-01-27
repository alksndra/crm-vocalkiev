# Vocal Kiev CRM system on Django

The system makes it easy to track all the moments of education at this school


## Features

What's all the bells and whistles this project can perform?
1. It is convenient for the administrator to register new clients,
- register payment for training or rent,
- assign paid subscriptions to clients
2. All users have a convenient schedule
3. Еhe ability to post comments to lessons, to clients, to teachers.
4. The ability to keep track of the number of remaining lessons in the purchased subscription.


## Installing

```
python -m venv new_project
source bin/activate
sudo apt install python3
pip install Django==3.2.5
git clone https://github.com/alksndra/vocalkiev-crm.git

```


## Deploy

### pythonanywhere

```shell
rm -rf vocalkiev-crm
wget https://github.com/alksndra/vocalkiev-crm-django/archive/refs/heads/main.zip
unzip main.zip
mv vocalkiev-crm-django-main/ vocalkiev-crm
rm main.zip
cd vocalkiev-crm
python manage.py migrate
python manage.py loaddata fixtures/fixtures.json
django-admin compilemessages
python manage.py collectstatic
```

and reboot App

### localhost

```shell
python3 -m venv vocalkiev-crm-django-env
cd vocalkiev-crm-django-env/
source bin/activate
python -m pip install -r requirements.txt
git clone git@github.com:lobanov-oleh/vocalkiev-crm-django.git
cd vocalkiev-crm-django/
```

```shell
python manage.py migrate
python manage.py loaddata fixtures/fixtures.json
django-admin compilemessages
python manage.py collectstatic
python manage.py runserver
```


## Licensing

The code in this project is licensed under MIT license.
It is a permissive license, that is, it allows the licensed code to be used in a proprietary software package, provided that the license is provided with this software world.
