#syntax=docker/dockerfile:1

FROM python:3.9.7-slim

# Configure APT so it doesn't pull man pages
RUN echo APT::Install-Recommends "0"; APT::Install-Suggests "0"; >> /etc/apt/apt.conf

# Install the necessary stuff to build any pip packages from source, just in case
# the wheel is unavailable for some reason
RUN apt-get update && apt-get install -y build-essential libffi-dev libxml2-dev libxslt-dev redis\
    default-mysql-client default-libmysqlclient-dev

# Disable python bytecode to reduce disk size
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies that all images will depend on
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Aggressively remove things to get the image size down
# Shouldn't be necessary due to disabling py bytecode, but just in case
RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip
# https://wiki.debian.org/ReduceDebian#Remove_unwanted_files_at_install_time:wiki
RUN apt-get purge $(aptitude search '~i!~M!~prequired!~pimportant!~R~prequired!~R~R~prequired!~R~pimportant!~R~R~pimportant!busybox!grub!initramfs-tools' | awk '{print $2}') &&\
    apt-get purge aptitude && \
    apt-get autoremove && \
    apt-get clean
# Again, shouldn't be necessary due to disabling man pages, but still
RUN rm -Rf /usr/share/man/??_*

# Remove existing requirements so image consumers can use their own
RUN rm requirements.txt