FROM python:3

EXPOSE 8000

RUN apt-get update && apt-get install -y gettext

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

RUN python manage.py compilemessages

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
