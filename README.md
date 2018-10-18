# shackbureau

shackbureau was the shackspace membership management software. It was retired in favor of
[byro](https://github.com/byro/byro).

[![Build Status](https://travis-ci.org/shackspace/shackbureau.svg?branch=master)](https://travis-ci.org/shackspace/shackbureau)

## howto run

### docker-compose

#### Install docker-compose
    sudo pip install -U docker-compose

#### Make an alias
    alias dc=docker-compose

### Build the container
    dc build

#### db reset
    dc run --rm web reset_db

#### (re-)create database structure
    dc run --rm web migrate

#### createsuperuser
    dc run --rm web createsuperuser

### start the containter
    dc up -d
And navigate your browser to `http://localhost:8000/admin/`

## Importing old data

Export the CSV from LibreOffice, delimiter `;` quote-char `"` and move it to the root of this git repo.

Run `dc run --rm web shell_plus `

    from usermanagement.utils import import_old_shit
    import_old_shit('/opt/code/Mitglieder.csv')

## view logs
    dc logs [web|db|data]

## Testing

### run tests
    docker exec -ti shackbureau_web_1 py.test
