# Vehicles API

## Installation

### Prerequisites

- [Python](https://www.python.org/)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)

### Installation instructions

1. After downloading the project create and fill out the local settings file:

    ```
    cp config/env.local.example config/.env
    ```

2. Configure your local database by filling out `DJANGO_DATABASE_URL` setting in `.env` file. Make sure the username, password, and database name match the environment variables in docker-compose.yml

3. After downloading the project and filling out the env file create and enter a Docker image

    ```
    docker-compose up
    ```

4. Run test command to make sure everything is in order:

        docker-compose run web ./manage.py test

5. Start the development server:

        docker-compose up
        or
        docker-compose run web ./manage.py runserver
