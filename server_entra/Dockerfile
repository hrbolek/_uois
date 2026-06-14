FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV INDEX_HTML_PATH=/app/index.html
ENV APOLLO_GQL_URL=http://apollo:3000/api/gql/
ENV AUTH_COOKIE_NAME=authorization
ENV INTERNAL_JWT_ISSUER=frontend-bridge-internal-oauth
ENV INTERNAL_JWT_TTL_SECONDS=3600
ENV HTTP_TIMEOUT_SECONDS=30

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY main.py /app/main.py
COPY index.html /app/index.html

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
