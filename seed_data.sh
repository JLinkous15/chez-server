rm -rf chezapi/migrations
rm db.sqlite3
python manage.py makemigrations chezapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata chefs
python manage.py loaddata cheeses
python manage.py loaddata chezzes
python manage.py loaddata comments
