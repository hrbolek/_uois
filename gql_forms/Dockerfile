# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster as prepare

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# FROM prepare as tester
RUN python -m pip install coverage
# RUN python -m unittest tests/*
RUN python -m coverage run -m unittest -v tests/*
RUN python -m coverage report

FROM prepare as runner
# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--reload=True", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-t", "60", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
