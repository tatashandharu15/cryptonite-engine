# syntax=docker/dockerfile:1.7

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN python -m pip install --upgrade pip \
    && pip install .

FROM base AS dev
RUN pip install .[dev]

FROM base AS worker
CMD ["celery", "-A", "workers.celery", "worker", "--loglevel=INFO"]

FROM base AS beat
CMD ["celery", "-A", "workers.celery", "beat", "--loglevel=INFO"]
