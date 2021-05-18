# Start from an official ubuntu image
FROM ubuntu
# Specify the command to be run inside the container at installation
RUN apt-get update && apt-get install -y python3 python3-pip iputils-ping
# Add some files to the image from the host
ADD ./agent.py /root/
ADD ./requirements.txt /root/

# Run at startup the following commands
RUN pip install -r /root/requirements.txt
# This variable forces pikato print something out
ENV PYTHONUNBUFFERED=1
CMD ["/usr/bin/python3", "/root/agent.py"]

