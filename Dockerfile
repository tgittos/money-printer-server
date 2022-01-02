#syntax=docker/dockerfile:1

FROM git.gittos.net:5050/money-printer/money-printer-infrastructure/money-printer:latest

# Accept an environment arg to deploy to different environments
ARG environment

# Disable python bytecode to reduce disk size
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
# use the cache, because we build our own base image to speed this up
RUN pip install -r requirements.txt

# Copy core app code required to run the app
COPY src src
COPY bin bin
COPY config.json config.json

# Testing specific config files
COPY .coveragerc .coveragerc
COPY pytest.ini pytest.ini

# Create a logs dir
RUN mkdir logs

# Expose the port that the app runs on
EXPOSE 80
EXPOSE 443

# If an environment _wasn't_ passed in, default to development
ENV MP_ENVIRONMENT=development
# Bind to the public IP of the container
ENV MP_HOST=0.0.0.0
ENV MP_PORT=80
# Add our current path to the Python path
ENV PYTHONPATH=$PYTHONPATH:src