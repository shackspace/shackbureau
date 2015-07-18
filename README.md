# shackbureau
the one and only (yet another) shack member managment




## howto run

### docker-compose

(add here please)

#### db reset
docker-compose run web python3 manage.py reset_db

#### database reset
docker-compose run web python3 manage.py migrate

#### createsuperuser
docker-compose run web python3 manage.py createsuperuser
