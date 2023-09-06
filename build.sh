set -o errexit  # exit on error

pip install -r requirements.txt
pip install git+https://github.com/benslavin/django-db-prefix.git

python manage.py migrate
