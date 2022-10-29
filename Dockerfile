FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD . /opt/app
WORKDIR /opt/app

RUN pip install pipenv
RUN pipenv install --system --deploy

EXPOSE 8001
