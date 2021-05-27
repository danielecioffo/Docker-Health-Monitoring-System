# Install all the requirements for the Agent
pip3 install -r Agent/requirements.txt

# Start three dummy containers
docker build -t dummy Dummy\ Container/
docker run -d --name dummy_one --cap-add=NET_ADMIN dummy
docker run -d --name dummy_two --cap-add=NET_ADMIN dummy
docker run -d --name dummy_three --cap-add=NET_ADMIN dummy

# Start health monitoring agent
python3 Agent/agent.py &

# Start antagonist
docker build -t antagonist Antagonist/
docker run -d --name antagonist -v /var/run/docker.sock:/var/run/docker.sock antagonist