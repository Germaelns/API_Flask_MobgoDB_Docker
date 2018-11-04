FROM python:3-onbuild
ADD . /todo
WORKDIR /todo
RUN pip3 install -r requirements.txt