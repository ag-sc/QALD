FROM: nginx:alpine

ADD https://github.com/aparcar/QALD/archive/master.zip master.zip

RUN unzip master.zip -d /usr/share/nginx/html/

