
FROM debian:stretch
RUN apt-get update
RUN apt-get install -y python3 python-virtualenv mongodb rabbitmq-server \
                       redis-server supervisor strace

RUN useradd -m chirp
COPY . /home/chirp/chirp
RUN virtualenv -p python3 /home/chirp/venv
RUN /home/chirp/venv/bin/pip install -r /home/chirp/chirp/requirements.txt

EXPOSE 80
USER root
CMD ["/usr/bin/supervisord", "-nc", "/home/chirp/chirp/docker/supervisor.conf"]
