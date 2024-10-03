FROM apache/airflow:2.7.2
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
USER airflow