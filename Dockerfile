FROM python:3

EXPOSE 8000

RUN apt-get update && apt-get install -y gettext

WORKDIR /usr/src/app

COPY docker-entrypoint.sh /usr/src/app-sh/
RUN chmod +x /usr/src/app-sh/docker-entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py compilemessages

ENTRYPOINT ["/usr/src/app-sh/docker-entrypoint.sh"]
