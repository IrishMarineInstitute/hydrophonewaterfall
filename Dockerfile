FROM ipython/scipystack
MAINTAINER Damian Smyth <damian.smyth@marine.ie>
COPY apt.conf /etc/apt/apt.conf
ENV http_proxy http://10.0.5.55:80
ENV https_proxy http://10.0.5.55:80
RUN apt-get update
RUN apt-get -y install wget
RUN http_proxy=http://10.0.5.55:80 https_proxy=http://10.0.5.55:80 pip2 install bottle bottle-fdsend schedule
COPY app.py app.py
CMD ["./app.py"]
EXPOSE 80
