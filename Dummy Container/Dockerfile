# Start from an official ubuntu image
FROM ubuntu
# Specify the command to be run inside the container at installation
RUN apt-get update && apt-get install -y python3 python3-pip iproute2
# Add some files to the image from the host
ADD ./dummy.py /root/
ADD ./antagonist.py /root/
ADD ./start.sh /root/

# Run at startup the following commands
CMD ["/bin/bash", "/root/start.sh"]
