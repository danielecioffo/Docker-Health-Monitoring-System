# Stop health monitoring agent
#docker stop agent

# Remove agent
#docker rm agent

pkill python3

# Stop antagonist
docker stop antagonist

# Remove antagonist
docker rm antagonist

# Stop dummy containers
docker stop dummy_one
docker stop dummy_two
docker stop dummy_three

# Remove dummy containers
docker rm dummy_one
docker rm dummy_two
docker rm dummy_three

# Stop REST
docker stop swagger_server

# Remove REST
docker rm swagger_server
