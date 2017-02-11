FROM python:3.6
MAINTAINER shackspace

EXPOSE 8000

ENV DEBIAN_FRONTEND noninteractive

USER root
RUN apt-get update -y && apt-get install -y \
    bash\
    curl\
    git\
    lib32z1-dev\
    libfreetype6-dev\
    libjpeg-dev\
    locales\
    postgresql-server-dev-all\
    postgresql-client\
    zlib1g-dev

RUN apt-get install --no-install-recommends -y \
    lmodern\
    texlive\
    texlive-lang-german\
    texlive-latex-extra

# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install -Ur requirements.txt
ADD . /opt/code

RUN useradd uid1000 -d /home/uid1000
RUN mkdir -p /home/uid1000 && chown uid1000: /home/uid1000

USER uid1000

WORKDIR shackbureau
