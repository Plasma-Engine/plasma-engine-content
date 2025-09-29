FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["/root/.local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

