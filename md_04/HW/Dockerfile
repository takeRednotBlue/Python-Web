# DOCKER COMMANDS
# docker build . -t maksymklym/test-web-servers
# docker run -d -p 3000:3000 -v /home/maksymklym/Documents/storage:/storage maksymklym/test-web-servers

FROM python:3.11

ENV APP_HOME /app
ENV STORAGE_DIR /storage

WORKDIR $APP_HOME

RUN mkdir ${STORAGE_DIR}

COPY . .

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]