FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install dbt-core==1.7.10 dbt-spark[PyHive]==1.7.1

# Install dbt dependencies (as specified in packages.yml file)
# Build seeds, models and snapshots (and run tests wherever applicable)
CMD dbt deps && dbt build --profiles-dir profiles
