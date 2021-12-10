#syntax=docker/dockerfile:1

FROM tgittos/money-printer:latest

# Accept an environment arg to deploy to different environments
ARG environment

# Disable python bytecode to reduce disk size
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir app

# Install dependencies
COPY requirements.txt app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy core app code required to run the app
COPY core app/core
COPY server app/server
COPY tests app/tests
COPY config* app/.
# TODO refactor this to external env vars
COPY .secrets.json app/.secrets.json

# Create a logs dir
RUN mkdir app/logs

# Expose the port that the app runs on
EXPOSE 80
EXPOSE 443

# If an environment _wasn't_ passed in, default to development
ENV MP_ENVIRONMENT=environment:-development
# Bind to the public IP of the container
ENV MP_HOST=0.0.0.0
ENV MP_PORT=80
# Add our current path to the Python path
ENV PYTHONPATH=$PYTHONPATH:/app

ENTRYPOINT cd app && python ./server/bin/api.py && tail -f ./server/logs/mp.log