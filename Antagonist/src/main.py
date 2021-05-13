import docker

if __name__ == '__main__':
    client = docker.from_env()
    list_of_containers = client.containers.list()
    print('List of containers: ' + list_of_containers + '\n')
    for container in list_of_containers:
        print('Container ID: ' + container.id + '\n')
        container.restart()
