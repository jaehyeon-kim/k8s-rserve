FROM rocker/r-ver:3.6

ARG RS_VERSION
ENV RS_VERSION=${RS_VERSION:-1.8-6}

## install rserve
RUN apt-get update && apt-get install -y libssl-dev wget
RUN wget http://www.rforge.net/Rserve/snapshot/Rserve_${RS_VERSION}.tar.gz \
    && R CMD INSTALL Rserve_${RS_VERSION}.tar.gz

## create a user
RUN useradd rserve && mkdir /home/rserve \
	&& chown rserve:rserve /home/rserve

## copy source
COPY . /home/docker/

ENTRYPOINT ["/usr/local/bin/R", "CMD", "Rserve", "--slave", "--RS-conf", "${RS_CONF}", "--RS-source", "${RS_SRC}"]
