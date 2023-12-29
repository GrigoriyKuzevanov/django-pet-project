FROM python:3.9

COPY . ./app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait

RUN chmod +x /wait

ENTRYPOINT bash ./entrypoint.sh