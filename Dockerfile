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

# Set production environment for nodejs application
ENV NODE_ENV=production

COPY package*.json /usr/src/app/
RUN npm install

COPY . /usr/src/app/

# Generate "static/js/*.js" from "src/js/*.js"
RUN /usr/src/app/node_modules/.bin/gulp

EXPOSE 8000

CMD [ "gunicorn", "main:app", "--log-file=-", "--bind=0.0.0.0:8000" ]
