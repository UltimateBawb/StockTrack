STOCKTRACK

Symbol lists: ftp://ftp.nasdaqtrader.com/symboldirectory

Setup database:

> $ sudo apt update

> $ sudo apt install postgresql postgresql-contrib

> $ sudo -u postgres psql

> postgres=# ALTER USER postgres PASSWORD "postgres";

> postgres=# CREATE USER <username>

> postgres=# CREATE DATABASE stocktrack

> postgres=# \i setup.sql

Setup libraries:

> $ sudo apt-get install python-psycopg2

> $ sudo apt-get install libpq-dev

> $ pip3 install psycopg2

> $ pip3 install yfinance --upgrade --no-cache-dir

