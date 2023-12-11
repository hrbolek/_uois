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
# First phase
#
###############################################################
FROM node:16 as buildnode

# Create app directory
WORKDIR /usr/src

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY jsconfig.json jsconfig.json
COPY packages ./packages

###############################################################
#
# Second phase
#
###############################################################
FROM buildnode as appdev

WORKDIR /usr/src
COPY apps/dev ./apps/dev
RUN npm install
WORKDIR /usr/src/apps/dev
RUN npm run build3

###############################################################
#
# Third phase
#
###############################################################
# FROM buildnode as appstorybook

# WORKDIR /usr/src
# COPY apps/storybook ./apps/storybook
# RUN npm install
# WORKDIR /usr/src/apps/storybook
# RUN npm run build

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

WORKDIR /app/js
# COPY --from=buildnode /usr/src/app/build/ /app/js/
COPY --from=appdev /usr/src/apps/dev/build/ /app/js/

# WORKDIR /app/storybook
# # COPY --from=buildnode /usr/src/app/build/ /app/js/
# COPY --from=appstorybook /usr/src/apps/storybook/dist/ /app/storybook/

WORKDIR /app/pyserver
COPY ./pyserver/ /app/pyserver
WORKDIR /app

# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "pyserver.app:app"]
#CMD ["gunicorn", "--reload", "--reload-engine", "inotify", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
