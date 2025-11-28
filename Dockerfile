FROM python:3.13.2
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /scripts/
RUN pip install --upgrade pip
RUN pip install -r /scripts/requirements.txt
