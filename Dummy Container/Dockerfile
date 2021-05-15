# Start from an official ubuntu image
FROM ubuntu
# Specify the command to be run inside the container at installation
RUN apt-get update && apt-get install -y python3 python3-pip
# Add some files to the image from the host
ADD ./dummy.py /root/

# Run at startup the following commands
CMD ["/usr/bin/python3", "/root/dummy.py"]
