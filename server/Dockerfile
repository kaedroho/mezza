FROM node:18.17.1-bullseye-slim as client

# Install client dependencies
COPY client/package.json client/package-lock.json /client/
RUN cd /client && npm install

# Copy the source code of the client into the container.
COPY client /client

# Build the client
RUN cd /client && npm run build

FROM python:3.12.3-slim-bookworm AS base

RUN apt update -y \
    && apt install -y --no-install-recommends \
    # Required to build psycopg2
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONPATH=/server \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=mezza.settings \
    BASE_URL=http://localhost:8000 \
    PORT=8000

# Add user that will be used in the container
ARG UID=1000
RUN useradd mezza --uid ${UID} --create-home && mkdir /server $VIRTUAL_ENV && chown -R mezza /server $VIRTUAL_ENV

# Install poetry
RUN pip install poetry==1.8.3

# Use user "mezza" to run the build commands below and the server itself.
USER mezza

# Use /server folder as a directory where the source code is stored.
WORKDIR /server

# Set up virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install Python dependencies
COPY --chown=mezza server/pyproject.toml server/poetry.lock ./
RUN poetry install --no-root --only main

# Copy the source code of the project into the container.
COPY --chown=mezza server .

# Run poetry install again to install our project
RUN poetry install --only main

FROM base as prod

# Copy the client bundle from the client target
COPY --chown=mezza --from=client /client/dist /client

# Collect static files
ENV VITE_BUNDLE_DIR=/client
RUN DJANGO_SECRET_KEY=secret python manage.py collectstatic --noinput --clear

CMD django-admin migrate && gunicorn -w 4 --threads 2 mezza.wsgi:application

FROM base AS dev

# Install dev dependencies
RUN poetry install
