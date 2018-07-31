# Dockerfile
#
# https://nodejs.org/en/docs/guides/nodejs-docker-webapp/

FROM node:8.11.3-stretch

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python2.7 \
        python-pip \
        python-setuptools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json gulpfile.js src /usr/src/app/
RUN npm install --only=production

COPY . /usr/src/app/

EXPOSE 8000

CMD [ "gunicorn", "main:app", "--log-file=-", "--bind=0.0.0.0:8000" ]
