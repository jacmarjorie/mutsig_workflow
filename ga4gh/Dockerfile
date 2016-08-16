FROM phusion/baseimage

ENV GA4GH_CLIENT_DIR /opt/ga4gh_client

ADD . /

WORKDIR $GA4GH_CLIENT_DIR

RUN apt-get -qq update

RUN apt-get install -y \
	python-dev \
	python-setuptools \
	wget 

RUN easy_install pip && pip install \
	requests 

RUN wget https://raw.githubusercontent.com/jacmarjorie/ga4gh_galaxy_interface/harmony_point/ga4gh_hp_client.py

