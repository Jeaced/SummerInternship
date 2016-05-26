Do this stuff:

-1)Clone repo

0)Launch postgres (Be sure it's running on port 5432)

1)Open terminal:

	$sudo -i -u postgres

	Enter your password

	createuser -P -s -e admin
	(for password use "qwerty123". Without quotes ofc)

	$psql

	$create database project_db

2)Open another terminal window:

	Go to directory with manage.py inside

	$python3 manage.py migrate

3)To run server:

	$python3 manage.py runserver

	It's running on port 8000                (127.0.0.1:8000)	

4)Every time there are new migrations in migrations folder don't forget to do step (2)	

5)Enjoy