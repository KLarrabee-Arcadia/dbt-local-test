FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends

WORKDIR /usr/src/app

# Install the dbt Postgres adapter. This step will also install dbt-core
RUN pip install --upgrade pip
# RUN pip install pytz==2024.1 dbt-postgres==1.3.1
RUN pip install dbt-core==1.7.10 dbt-spark[PyHive]==1.7.1

# Install dbt dependencies (as specified in packages.yml file)
# Build seeds, models and snapshots (and run tests wherever applicable)
CMD dbt deps && dbt build --profiles-dir profiles
