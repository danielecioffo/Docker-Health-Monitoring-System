# Start three dummy containers
docker build -t dummy Dummy\ Container/
docker run -d --name dummy_one dummy
docker run -d --name dummy_two dummy
docker run -d --name dummy_three dummy

# Start health monitoring agent
docker build -t agent Agent/
docker run -d --name agent -v /var/run/docker.sock:/var/run/docker.sock agent

# Start antagonist
docker build -t antagonist Antagonist/
docker run -d --name antagonist --cap-add=NET_ADMIN -v /var/run/docker.sock:/var/run/docker.sock antagonist

