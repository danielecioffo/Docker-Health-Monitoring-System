# Start three dummy containers
cd dummy
docker build -t dummy .
cd ..
docker run -d --name dummy_one dummy
docker run -d --name dummy_two dummy
docker run -d --name dummy_three dummy

# Start health monitoring agent
cd agent
docker build -t agent .
cd ..
docker run -d --name agent -v /var/run/docker.sock:/var/run/docker.sock agent
