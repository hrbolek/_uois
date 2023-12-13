###############################################################
#
# Zero phase
#
###############################################################
FROM python:3.9-slim-buster as pythonbase

# instalace curl, aby bylo mozne zprovoznit standardni healthcheck
RUN apt update && apt install curl -y && rm -rf /var/cache/apk/*

# Install pip requirements
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

###############################################################
#
# Last phase
#
###############################################################
FROM pythonbase as executepython

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


WORKDIR /app
COPY . /app

# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "server.main:app"]
#CMD ["gunicorn", "--reload", "--reload-engine", "inotify", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
