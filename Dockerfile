FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv --no-cache-dir && pipenv install --dev --system --deploy && pipenv --clear

COPY . /code/

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

EXPOSE 8000
