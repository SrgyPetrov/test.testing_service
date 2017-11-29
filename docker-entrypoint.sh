#!/bin/bash
set -e

case "$1" in
	"runserver")
		python manage.py migrate --noinput
        python manage.py loaddata users quizzes -i
		python manage.py runserver 0.0.0.0:8000
	;;
	"runtests")
		py.test -x /usr/src/app/tests/
	;;
    "shell")
		python manage.py shell
	;;
	*)
		exec "$@"
esac
