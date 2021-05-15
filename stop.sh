# Stop dummy containers
docker stop dummy_one
docker stop dummy_two
docker stop dummy_three

# Remove dummy containers
docker rm dummy_one
docker rm dummy_two
docker rm dummy_three

# Stop health monitoring agent
docker stop agent

# Remove agent
docker rm agent
