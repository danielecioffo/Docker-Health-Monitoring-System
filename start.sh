#if not present, install docker module for python
pip3 install docker
pip3 install six

#install pika, to be used for rabbitMq communication with broker
pip3 install pika

# Start three dummy containers
docker build -t dummy Dummy\ Container/
docker run -d --name dummy_one --cap-add=NET_ADMIN dummy
docker run -d --name dummy_two --cap-add=NET_ADMIN dummy
docker run -d --name dummy_three --cap-add=NET_ADMIN dummy

# Start health monitoring agent
#docker build -t agent Agent/
#docker run -d --name agent -v /var/run/docker.sock:/var/run/docker.sock agent
python3 Agent/agent.py &

# Start antagonist
docker build -t antagonist Antagonist/
docker run -d --name antagonist -v /var/run/docker.sock:/var/run/docker.sock antagonist

# Start REST
docker build -t swagger_server Rest/
docker run --name swagger_server -p 8080:8080 swagger_server