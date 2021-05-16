FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip iproute2
ADD ./antagonist.py /root/
ADD ./requirements.txt /root/
RUN pip install -r /root/requirements.txt
CMD ["/usr/bin/python3", "/root/antagonist.py"]
